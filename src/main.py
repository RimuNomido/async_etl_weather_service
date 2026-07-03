from src.collectors import OpenWeatherCollector
from src.crud import add_city, add_weather_data, add_weather_source
from src.utils import get_coords
from dotenv import load_dotenv
from functools import wraps
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
    coords = get_coords(city)
    if coords is None:
        print('Не удалось получить координаты.')
        return None

    owc = OpenWeatherCollector(WEATHER_MAP_API, city=city, lat=coords[0], lon=coords[1])
    data = await owc.send_request()
    weather_data = owc.parse_response(data)
    return weather_data

@app.command()
@unasync
async def main(cities: list[str] = typer.Option(
                ['Тюмень', 'Москва', 'Санкт-Петербург'],
                '--cities',
                '-c',
                help='Список городов для сбора погоды',
            )):
    tasks = [get_weather_owm(city) for city in cities]
    weather_list = await asyncio.gather(*tasks)
    for city, weather_data in zip(cities, weather_list):
        if weather_data:
            typer.echo(f'Погода в {city}: {weather_data}')

if __name__ == '__main__':
    app()