from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential
import httpx

class OpenWeatherCollector:
    def __init__(self, api_key, city, lat, lon):
        self.api_key = api_key
        self.city = city
        self.lat = lat
        self.lon = lon
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def send_request(self):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.api_key}&units=metric"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

        return response.json()
    
    def parse_response(self, response):
        weather_data = response
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        pressure = weather_data['main']['pressure']
        date = datetime.fromtimestamp(weather_data['dt'])
        timestamp = date.strftime('%Y-%m-%d %H:%M:%S')
        
        parsed_data = {
            'temp': temp,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'pressure': pressure,
            'timestamp': timestamp
        }

        return parsed_data