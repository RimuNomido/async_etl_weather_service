from sqlalchemy import select, update, delete
from src.models import City, WeatherData, WeatherSource
from src.database import AsyncSessionLocal

async def add_city(name, lat, lon):
    async with AsyncSessionLocal() as session:
        city = City(name=name, lat=lat, lon=lon)
        session.add(city)
        await session.commit()
        return city

async def get_city(name):
    async with AsyncSessionLocal() as session:
        stmt = select(City).where(City.name == name)
        result = await session.scalar(stmt)
        return result

async def delete_city(name):
    async with AsyncSessionLocal() as session:
        stmt = delete(City).where(City.name == name)
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount > 0

async def add_weather_source(name, base_url):
    async with AsyncSessionLocal() as session:
        weather_source = WeatherSource(name=name, base_url=base_url)
        session.add(weather_source)
        await session.commit()
        return weather_source

async def get_weather_source(name):
    async with AsyncSessionLocal() as session:
        stmt = select(WeatherSource).where(WeatherSource.name == name)
        result = await session.scalar(stmt)
        return result
    
async def delete_weather_source(name):
    async with AsyncSessionLocal() as session:
        stmt = delete(WeatherSource).where(WeatherSource.name == name)
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount > 0
    
async def add_weather_data(city_id, source_id, temp, humidity, wind_speed, pressure, timestamp):
    async with AsyncSessionLocal() as session:
        weather_data = WeatherData(city_id=city_id,
                                   source_id=source_id,
                                   temp=temp,
                                   humidity=humidity,
                                   wind_speed=wind_speed,
                                   pressure=pressure,
                                   timestamp=timestamp)
        session.add(weather_data)
        await session.commit()
        return weather_data
    
async def get_weather_data(city_id, source_id):
    async with AsyncSessionLocal() as session:
        query = select(WeatherData).where(WeatherData.city_id == city_id,
                                         WeatherData.source_id == source_id)
        result = await session.execute(query)
        weather_list = result.scalars().all()
        return weather_list

async def delete_weather_data(city_id, source_id):
    async with AsyncSessionLocal() as session:
        stmt = delete(WeatherData).where(WeatherData.city_id == city_id,
                                         WeatherData.source_id == source_id)
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount > 0
    