from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class MonitoringTarget(Base):
    __tablename__ = "monitoring_targets"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, index=True)
    visa_type = Column(String, index=True)
    user_id = Column(Integer, index=True)
    config_json = Column(JSON)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)

    checks = relationship("CheckLog", back_populates="target")
    slots = relationship("SlotFound", back_populates="target")


class CheckLog(Base):
    __tablename__ = "check_log"

    id = Column(Integer, primary_key=True)
    target_id = Column(Integer, ForeignKey("monitoring_targets.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    proxy_used = Column(String, nullable=True)
    session_id = Column(String, nullable=True)
    status = Column(String)  # SLOT_FOUND, EMPTY, ERROR, CAPTCHA, CHECK_STARTED
    latency_ms = Column(Integer)
    message = Column(String, nullable=True)

    target = relationship("MonitoringTarget", back_populates="checks")


class SlotFound(Base):
    __tablename__ = "slots_found"

    id = Column(Integer, primary_key=True)
    target_id = Column(Integer, ForeignKey("monitoring_targets.id"))
    found_at = Column(DateTime, default=datetime.utcnow)
    slot_date = Column(DateTime)
    slot_time = Column(String)
    center = Column(String)
    score = Column(Integer)
    action = Column(String)  # NOTIFIED, BOOKED, IGNORED, EXPIRED
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=True)

    target = relationship("MonitoringTarget", back_populates="slots")
    booking = relationship("Booking", back_populates="slot", foreign_keys=[booking_id])


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String)  # IN_PROGRESS, SUCCESS, FAILED
    confirmation_number = Column(String, nullable=True)
    screenshot_path = Column(String, nullable=True)
    error_details = Column(String, nullable=True)

    slot = relationship("SlotFound", back_populates="booking", uselist=False)


class Proxy(Base):
    __tablename__ = "proxy_pool"

    id = Column(Integer, primary_key=True)
    ip_address = Column(String)
    port = Column(Integer)
    provider = Column(String)
    country = Column(String)
    last_used = Column(DateTime, nullable=True)
    success_count = Column(Integer, default=0)
    fail_count = Column(Integer, default=0)
    banned_until = Column(DateTime, nullable=True)
