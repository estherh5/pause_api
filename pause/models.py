import os

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import JSON, TEXT, TIMESTAMP


engine = create_engine(os.environ['DB_CONNECTION'])

Base = declarative_base()

Session = sessionmaker(bind=engine)


class Activities(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True, nullable=False)
    external_id = Column(TEXT, nullable=False)
    activities = Column(JSON, nullable=False)
    chart_types = Column(JSON, nullable=False)
    time_unit = Column(TEXT, nullable=False)
    month = Column(TEXT, nullable=True)
    year = Column(Integer, nullable=True)
    created = Column(TIMESTAMP(timezone=False), default=datetime.utcnow,
        nullable=False)
