import httpx
from fastapi import APIRouter, HTTPException

from backend.api.routes.utils import build_weather_query
from backend.db.crud import *


current_router = APIRouter(include_in_schema=True)

CURRENT_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"


@current_router.get("/current/")
async def get_weather_info(city: str, imperial=False):
    """Returns current weather info from OpenWeather's weather API.

    Args:
        city (str): Name of a city as collected by argparse
        imperial (bool): Use or not imperial units for temperature

    Returns:
        weather_info (dict~json): current weather info in specified city.
    """
    url = build_weather_query(base_url=CURRENT_WEATHER_API_URL, city=city, imperial=imperial)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        weather_info = response.json()
    return weather_info


@current_router.post("/current", response_model=WeatherSchema)
async def create_weather_report(report: WeatherSchema):
    """Created a new weather report"""
    weather_report = await get_by_city(city=report.city)
    if weather_report is not None:
        raise HTTPException(409, "The forecast already exists")
    weather_report = await create(report=report)
    return weather_report


@current_router.get("/current/{city}", response_model=WeatherSchema)
async def get_weather_by_city(city: str):
    weather_report = await get_by_city(city=city)
    if weather_report is None:
        raise HTTPException(404, "The forecast for current city is not found")
    return weather_report


@current_router.get("/current/all/", response_model=List[WeatherSchema])
async def get_all_reports():
    weather_reports = await get_all()
    if weather_reports is None:
        raise HTTPException(404, "Database is empty")
    return weather_reports


@current_router.put("/current/", response_model=WeatherSchema)
async def update_report(report: WeatherSchema):
    weather_report = await update(report=report)
    if weather_report is None:
        raise HTTPException(404, "There was an error updating the weather report.")
    return weather_report