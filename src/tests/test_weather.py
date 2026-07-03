from src.collectors import OpenWeatherCollector

def test_parse_response():
    expected = {'temp': 289.42, 'humidity': 95, 'wind_speed': 3.47, 'pressure': 1002, 'timestamp': '2026-07-03 15:23:26'}
    fake_response = {
                    'coord': {'lon': 65.52, 'lat': 57.15},
                    'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}],
                    'base': 'stations',
                    'main': {'temp': 289.42, 'feels_like': 289.58, 'temp_min': 289.42, 'temp_max': 289.42, 'pressure': 1002, 'humidity': 95, 'sea_level': 1002, 'grnd_level': 992},
                    'visibility': 10000,
                    'wind': {'speed': 3.47, 'deg': 318, 'gust': 6.82},
                    'clouds': {'all': 100},
                    'dt': 1783074206,
                    'sys': {'country': 'RU', 'sunrise': 1783032523, 'sunset': 1783096507},
                    'timezone': 18000, 
                    'id': 1488754, 
                    'name': 'Tyumen', 
                    'cod': 200
                    }
    owc = OpenWeatherCollector('fake_api', 'Tyumen', 57.15, 65.52)
    result = owc.parse_response(fake_response)
    assert expected == result