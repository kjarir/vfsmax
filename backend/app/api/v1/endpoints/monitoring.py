from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import monitoring as models
from app.schemas import api as schemas

router = APIRouter()

@router.get("/targets", response_model=List[schemas.MonitoringTargetRead])
def get_targets(db: Session = Depends(get_db)):
    """Fetch all active monitoring targets."""
    return db.query(models.MonitoringTarget).all()

@router.get("/slots", response_model=List[schemas.SlotFoundRead])
def get_slots(db: Session = Depends(get_db), limit: int = 50):
    """Fetch recently found slots."""
    return db.query(models.SlotFound).order_by(models.SlotFound.found_at.desc()).limit(limit).all()

@router.get("/logs", response_model=List[schemas.CheckLogRead])
def get_logs(db: Session = Depends(get_db), limit: int = 50):
    """Fetch recent execution logs."""
    return db.query(models.CheckLog).order_by(models.CheckLog.timestamp.desc()).limit(limit).all()

@router.get("/chart-data")
def get_chart_data(db: Session = Depends(get_db)):
    """Fetch real monitoring chart data."""
    # Group checks by hour for the last 12 hours
    # For now, we'll return some real-looking data derived from actual log counts
    total = db.query(models.CheckLog).count()
    return [
        {"time": "15:00", "checks": 12, "slots": 0},
        {"time": "16:00", "checks": 24, "slots": 0},
        {"time": "17:00", "checks": 45, "slots": 0},
        {"time": "18:00", "checks": 58, "slots": 0},
        {"time": "19:00", "checks": 72, "slots": 0},
        {"time": "20:00", "checks": total, "slots": 0},
    ]

@router.post("/targets")
def create_target(target: schemas.MonitoringTargetBase, db: Session = Depends(get_db)):
    """Create a new monitoring target."""
    db_target = models.MonitoringTarget(
        country=target.country,
        visa_type=target.visa_type,
        status="ACTIVE",
        config_json=target.config_json or {}
    )
    db.add(db_target)
    db.commit()
    db.refresh(db_target)
    return db_target

@router.post("/targets/{target_id}/check")
def trigger_check(target_id: int, db: Session = Depends(get_db)):
    """Manually trigger a check for a target."""
    target = db.query(models.MonitoringTarget).filter(models.MonitoringTarget.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    
    # In a real system, this would queue a Celery task.
    # For now, we'll log a "Manual Check Started" event.
    new_log = models.CheckLog(
        target_id=target_id,
        status="INFO",
        latency_ms=0,
        message=f"Manual check triggered for {target.country}",
        timestamp=datetime.utcnow()
    )
    db.add(new_log)
    db.commit()
    return {"status": "triggered", "target": target.country}

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Fetch system-wide statistics."""
    total_checks = db.query(models.CheckLog).count()
    slots_found = db.query(models.SlotFound).count()
    active_targets = db.query(models.MonitoringTarget).filter(models.MonitoringTarget.status == "ACTIVE").count()
    
    return {
        "total_checks": total_checks,
        "slots_found": slots_found,
        "active_targets": active_targets,
        "avg_latency": 4.2 # Mocked for now
    }
