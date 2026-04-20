from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

# Database setup
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./event_management.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Database Models
class ZoneSnapshot(Base):
    """Historical snapshot of zone metrics"""
    __tablename__ = "zone_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    zone_name = Column(String, index=True)
    density = Column(Float)
    wait_time = Column(Integer)
    status = Column(String)
    capacity = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    """Alert/notification records"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    zone_name = Column(String, index=True)
    alert_type = Column(String)  # "bottleneck", "capacity", "wait_time"
    severity = Column(String)  # "low", "medium", "high", "critical"
    message = Column(Text)
    is_read = Column(Integer, default=0)  # 0 = unread, 1 = read
    timestamp = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    """Audit log for user actions"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    action = Column(String)
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
