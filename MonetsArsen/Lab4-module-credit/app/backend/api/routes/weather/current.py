import httpx
from fastapi import APIRouter, HTTPException

from backend.api.routes.utils import build_weather_query
from backend.db.crud import *
from datetime import datetime


current_router = APIRouter(include_in_schema=True)

CURRENT_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"


@current_router.get("/current/")
async def get_weather_info(city: str, imperial=False):
    """Fetches the current weather information for a given city from OpenWeather API.

    Args:
        city (str): The name of the city to fetch weather data for.
        imperial (bool): If True, returns the temperature in imperial units (Fahrenheit). Defaults to False.

    Returns:
        dict: A dictionary containing the current weather information for the city.
    """
    url = build_weather_query(base_url=CURRENT_WEATHER_API_URL, city=city, imperial=imperial)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        weather_info = response.json()
    return weather_info


@current_router.post("/current", response_model=WeatherSchema)
async def create_weather_report(report: WeatherSchema):
    """Creates a new weather report and stores it in the database.

    Args:
        report (WeatherSchema): A schema object containing the weather data to be stored.

    Returns:
        WeatherSchema: The weather report that was created.

    Raises:
        HTTPException: If a report for the given city already exists, a 409 error is raised.
    """
    weather_report = await get_by_city(city=report.city)
    if weather_report is not None:
        raise HTTPException(409, "The forecast already exists")
    weather_report = await create(report=report)
    return weather_report


@current_router.get("/current/{city}", response_model=WeatherSchema)
async def get_weather_by_city(city: str):
    """Fetches the weather report for a specific city.

    Args:
        city (str): The name of the city for which the weather report is to be retrieved.

    Returns:
        WeatherSchema: The weather report for the specified city.

    Raises:
        HTTPException: If no weather report is found for the city, a 404 error is raised.
    """
    weather_report = await get_by_city(city=city)
    if weather_report is None:
        raise HTTPException(404, "The forecast for current city is not found")
    return weather_report


@current_router.get("/current/all/", response_model=List[WeatherSchema])
async def get_all_reports():
    """Fetches all weather reports stored in the database.

    Returns:
        List[WeatherSchema]: A list of all weather reports in the database.

    Raises:
        HTTPException: If the database is empty, a 404 error is raised.
    """
    weather_reports = await get_all()
    if weather_reports is None:
        raise HTTPException(404, "Database is empty")
    return weather_reports


@current_router.put("/current/", response_model=WeatherSchema)
async def update_report(report: WeatherSchema):
    """Updates an existing weather report with new data.

    Args:
        report (WeatherSchema): The updated weather data to be stored.

    Returns:
        WeatherSchema: The updated weather report.

    Raises:
        HTTPException: If the update fails, a 404 error is raised.
    """
    weather_report = await update(report=report)
    if weather_report is None:
        raise HTTPException(404, "There was an error updating the weather report.")
    return weather_report


@current_router.post("/current/from_another_api", response_model=WeatherSchema)
async def create_weather_report_from_another_api(city: str):
    """Creates a new weather report from the OpenWeather API and stores it in the database.

    Args:
        city (str): The name of the city to fetch weather data for.

    Returns:
        WeatherSchema: The newly created weather report for the city.

    Raises:
        HTTPException:
            - If a report for the given city already exists, a 409 error is raised.
            - If the city is not found in OpenWeather API, a 404 error is raised.
    """
    weather_report = await get_by_city(city=city)
    if weather_report is not None:
        raise HTTPException(409, "The forecast already exists")

    url = build_weather_query(base_url=CURRENT_WEATHER_API_URL, city=city, imperial=False)

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        weather_info = response.json()

    if weather_info['cod'] == 404:
        raise HTTPException(409, "No such city")

    coordinates = (weather_info['coord']['lon'], weather_info['coord']['lat'])
    description = weather_info['weather'][0]['description']
    temperature = weather_info['main']['temp']
    humidity = weather_info['main']['humidity']
    wind_speed = weather_info['wind']['speed']

    time = datetime.now()

    sunrise = None
    sunset = None

    weather_data = WeatherSchema(
        city=city,
        coordinates=coordinates,
        description=description,
        temperature=temperature,
        humidity=humidity,
        wind_speed=wind_speed,
        time=time,
        sunrise=sunrise,
        sunset=sunset
    )

    weather_report = await create(report=weather_data)

    return weather_report

