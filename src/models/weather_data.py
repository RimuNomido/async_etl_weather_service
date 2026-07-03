from .base import Base
from sqlalchemy import Integer, Float, Column, DateTime

class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, nullable=False)
    source_id = Column(Integer, nullable=False)
    temp = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)