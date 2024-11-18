from urllib.parse import urlencode
import requests
from fastapi import APIRouter

from backend.config import WEATHER_API_KEY

pollution_router = APIRouter(include_in_schema=True)

router = APIRouter(include_in_schema=True)

POLLUTION_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/air_pollution"
