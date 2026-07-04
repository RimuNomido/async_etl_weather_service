from src.collectors import OpenWeatherCollector
from src.crud import add_city, add_weather_data, get_city, is_source_in_base
from src.utils import get_coords
from dotenv import load_dotenv
from typing import List
from functools import wraps
from typing_extensions import Annotated
import asyncio
import typer
import os

app = typer.Typer()

load_dotenv()

WEATHER_MAP_API = os.getenv('WEATHER_MAP_API')

def unasync(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper


async def get_weather_owm(city):
    db_city = await get_city(city)
    if db_city is None:
        coords = get_coords(city)
        if coords is None:
            print(f'Не удалось получить координаты для {city}.')
            return None

        db_city = await add_city(city, coords[0], coords[1])
    else:
        coords = (db_city.lat, db_city.lon)

    if coords is None:
        print('Не удалось получить координаты.')
        return None
    
    owc = OpenWeatherCollector(WEATHER_MAP_API, city=city, lat=coords[0], lon=coords[1])

    source = 'weather_map'
    db_source = await is_source_in_base(source, owc.url)
    data = await owc.send_request()
    weather_data = owc.parse_response(data)
    if weather_data:
        await add_weather_data(db_city.id, db_source.id, weather_data['temp'], weather_data['humidity'], weather_data['wind_speed'], weather_data['pressure'], weather_data['timestamp'])
        weather_data['timestamp'] = weather_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        return weather_data
    else:
        return None

@app.command()
@unasync
async def main(cities: Annotated[List[str], typer.Argument(help = "Список городов")] = ['Тюмень', 'Москва', 'Лондон']):
    tasks = [get_weather_owm(city) for city in cities]
    weather_list = await asyncio.gather(*tasks, return_exceptions=True)
    for city, weather_data in zip(cities, weather_list):
        if isinstance(weather_data, Exception):
            typer.echo(f'Ошибка для {city}: {weather_data}')
            continue
        if weather_data:
            typer.echo(f'Погода в {city}: {weather_data}')
        else:
            typer.echo(f'Нет данных для {city}')

if __name__ == '__main__':
    app()