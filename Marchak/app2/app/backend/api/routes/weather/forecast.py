import httpx
from fastapi import APIRouter

from backend.api.routes.utils import build_weather_query

forecast_router = APIRouter(include_in_schema=True)

FORECAST_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/forecast"


@forecast_router.get("/forecast/")
async def get_weather_forecast(city: str, imperial=False):
    """Returns current weather info from OpenWeather's weather API.

    Args:
        city (str): Name of a city as collected by argparse
        imperial (bool): Use or not imperial units for temperature

    Returns:
        weather_info (dict~json): current weather info in specified city.
    """
    url = build_weather_query(base_url=FORECAST_WEATHER_API_URL, city=city, imperial=imperial)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        weather_forecast = response.json()
    return weather_forecast
