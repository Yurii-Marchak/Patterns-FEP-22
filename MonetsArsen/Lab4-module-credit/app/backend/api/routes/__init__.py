from fastapi import APIRouter

# Importing the routers for different API sections
from backend.api.routes.sport.sports import sport_router
from backend.api.routes.weather.current import current_router
from backend.api.routes.weather.forecast import forecast_router
from backend.api.routes.weather.air_pollution import pollution_router


# Create an APIRouter instance to consolidate multiple routers into one
router = APIRouter()

# Include the current weather route, prefixing it with an empty string,
# and categorize it under the "current_weather" tag in the OpenAPI schema.
router.include_router(current_router, prefix="", tags=["current_weather"], include_in_schema=True)

# Include the weather forecast route, similarly with an empty prefix,
# and categorize it under the "weather_forecast" tag.
router.include_router(forecast_router, prefix="", tags=["weather_forecast"], include_in_schema=True)

# Include the air pollution route, with the "air_pollution" tag for API documentation.
router.include_router(pollution_router, prefix="", tags=["air_pollution"], include_in_schema=True)

# Include the sports news route, tagging it as "sport_news" for OpenAPI documentation.
router.include_router(sport_router, prefix="", tags=['sport_news'], include_in_schema=True)
