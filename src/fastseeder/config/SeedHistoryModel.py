from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class SeedHistoryModel(Base):
    __tablename__ = "seed_history"

    id = Column(String, primary_key=True)  # Unique name of the seed
    applied_at = Column(DateTime, default=datetime.utcnow)