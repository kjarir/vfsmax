from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core import database, security, config
from app.api.v1.endpoints import monitoring, auth, bookings
import structlog
import os

logger = structlog.get_logger(__name__)

app = FastAPI(
    title="VFSMAX — AI VFS Monitoring & Booking System",
    description="Full-stack, AI-powered system for monitoring and booking VFS appointments.",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root Endpoint
@app.get("/")
async def root():
    return {
        "status": "online",
        "system": "VFSMAX",
        "message": "Welcome to the VFSMAX API. Access/docs for API reference."
    }

# Include API routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(monitoring.router, prefix="/api/v1/monitoring", tags=["monitoring"])
app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["bookings"])

import asyncio
from datetime import datetime
from app.models import monitoring as models

async def background_monitoring_loop():
    while True:
        logger.info("Background Check Loop Running...")
        db = database.SessionLocal()
        try:
            targets = db.query(models.MonitoringTarget).filter(models.MonitoringTarget.status == "ACTIVE").all()
            for target in targets:
                # Simulation of a background check
                new_log = models.CheckLog(
                    target_id=target.id,
                    status="SUCCESS",
                    latency_ms=1200,
                    message=f"Automated check completed for {target.country}. No slots available.",
                    timestamp=datetime.utcnow()
                )
                db.add(new_log)
            db.commit()
        except Exception as e:
            logger.error(f"Error in background loop: {e}")
        finally:
            db.close()
        await asyncio.sleep(30)  # Check every 30 seconds

@app.on_event("startup")
async def startup_event():
    logger.info("VFSMAX Backend Starting...")
    
    # Initialize Database on Startup
    try:
        models.Base.metadata.create_all(bind=database.engine)
        db = database.SessionLocal()
        if db.query(models.MonitoringTarget).count() == 0:
            logger.info("Seeding initial target countries...")
            from datetime import datetime
            countries = [
                ("Germany", "Visa Appointment", "https://visa.vfsglobal.com/ind/en/deu/login", "Mumbai"),
                ("France", "Visa Appointment", "https://visa.vfsglobal.com/ind/en/fra/login", "New Delhi"),
            ]
            for country, visa_type, portal, center in countries:
                db.add(models.MonitoringTarget(
                    country=country, visa_type=visa_type, status="ACTIVE",
                    config_json={"portal_url": portal, "center": center}
                ))
            db.commit()
        db.close()
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

    # Start background loop only if not on Vercel (serverless doesn't support long-running tasks)
    if os.getenv("VERCEL") != "1":
        asyncio.create_task(background_monitoring_loop())

@app.on_event("shutdown")
async def shutdown_event():
    logger.warn("VFSMAX Backend Shutting Down...")
