from app.core.database import SessionLocal, engine
from app.models import monitoring as models
from datetime import datetime

def init_db():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if targets already exist
    if db.query(models.MonitoringTarget).count() == 0:
        print("Seeding ALL major VFS countries...")
        countries = [
            ("Germany", "Visa Appointment", "https://visa.vfsglobal.com/ind/en/deu/login", "Mumbai"),
            ("France", "Visa Appointment", "https://visa.vfsglobal.com/ind/en/fra/login", "New Delhi"),
            ("Spain", "Visa Appointment", "https://visa.vfsglobal.com/ind/en/esp/login", "Bengaluru"),
            ("Italy", "Visa Appointment", "https://visa.vfsglobal.com/ind/en/ita/login", "Mumbai"),
            ("Netherlands", "Visa Appointment", "https://visa.vfsglobal.com/ind/en/nld/login", "New Delhi"),
            ("Portugal", "Visa Appointment", "https://visa.vfsglobal.com/ind/en/prt/login", "Bengaluru")
        ]
        
        targets = []
        for country, visa_type, portal, center in countries:
            targets.append(
                models.MonitoringTarget(
                    country=country,
                    visa_type=visa_type,
                    status="ACTIVE",
                    config_json={
                        "portal_url": portal,
                        "id": f"{country.lower()}-{center.lower()}",
                        "name": visa_type,
                        "center": center,
                        "login_selectors": {
                            "email": "input[name='email']",
                            "password": "input[name='password']",
                            "submit": "button[type='submit']"
                        },
                        "booking_selectors": {
                            "slot_available": ".slot-available-indicator, .availability-message, .alert-success"
                        },
                        "vfs_email": "user@example.com",
                        "vfs_password": "password123"
                    }
                )
            )
        db.add_all(targets)
        db.commit()
        print(f"Database seeded with {len(targets)} countries.")

    
    db.close()

if __name__ == "__main__":
    init_db()
