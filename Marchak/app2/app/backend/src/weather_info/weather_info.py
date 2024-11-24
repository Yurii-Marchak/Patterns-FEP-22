import asyncio
from backend.api.routes.weather.current import get_weather_info


result_coroutine = get_weather_info(city="Lviv")
result = asyncio.run(result_coroutine)
print(result)