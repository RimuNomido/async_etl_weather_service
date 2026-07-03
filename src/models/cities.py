from sqlalchemy import String, Integer, Column, Float
from .base import Base

class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)