from typing import List, Optional
from backend.models.current_weather import WeatherSchema, WeatherReport


async def create(report: WeatherSchema) -> WeatherSchema:
    weather_report = WeatherReport(**report.model_dump())
    print(report.model_dump())
    await weather_report.insert()
    return report


async def get_by_city(city: str) -> Optional[WeatherReport]:
    weather_report = await WeatherReport.find_one(WeatherReport.city == city)
    return weather_report


async def get_all() -> List:
    reports = await WeatherReport.find_all().to_list()
    return reports


async def update(report: WeatherSchema) -> WeatherReport:
    to_update = await WeatherReport.find_one(WeatherReport.city == report.city)
    await to_update.set({WeatherReport.temperature: report.temperature,
                         WeatherReport.humidity: report.humidity,
                         WeatherReport.wind_speed: report.wind_speed,
                         WeatherReport.time: report.time})
    return to_update


async def delete(city: str) -> bool:
    to_delete = await WeatherReport.find_one(WeatherReport.city == city)
    if to_delete:
        await to_delete.delete()
        return True
