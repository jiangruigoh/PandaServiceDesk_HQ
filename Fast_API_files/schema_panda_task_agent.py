# coding: utf-8
from sqlalchemy import Column, DateTime, Index, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class TaskAgent(Base):
    __tablename__ = 'task_agent'
    __table_args__ = (
        Index('store_code', 'store_code', 'date_code', 'hourly_code', 'sequence', unique=True),
    )

    task_guid = Column(String(32), primary_key=True)
    task_type = Column(String(32), index=True)
    store_code = Column(String(10), nullable=False)
    date_code = Column(String(1), nullable=False, index=True)
    hourly_code = Column(String(2), nullable=False, index=True)
    sequence = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    task_status = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
