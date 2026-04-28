from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from .database import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text)
    schema_json = Column(JSONB)
    rows_json = Column(JSONB)
    chart_type = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())