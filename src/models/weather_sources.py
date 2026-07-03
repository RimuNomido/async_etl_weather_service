from .base import Base
from sqlalchemy import String, Integer, Column

class WeatherSource(Base):
    __tablename__ = 'weather_sources'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    base_url = Column(String, nullable=False)