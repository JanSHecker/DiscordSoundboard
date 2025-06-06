from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func

Base = declarative_base()

class Sound(Base):
    __tablename__ = "sounds"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
