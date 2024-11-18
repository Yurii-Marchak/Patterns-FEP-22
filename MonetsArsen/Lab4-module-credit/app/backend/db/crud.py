from typing import List, Optional
from backend.models.current_weather import WeatherSchema, WeatherReport
from backend.models.sport_event import SportsEventReport, SportsEventSchema


async def create(report: WeatherSchema) -> WeatherSchema:
    """
    Creates a new weather report in the database from the provided WeatherSchema.

    Args:
        report (WeatherSchema): The weather data to be stored.

    Returns:
        WeatherSchema: The original weather report schema that was passed in.
    """
    weather_report = WeatherReport(**report.model_dump())
    print(report.model_dump())
    await weather_report.insert()
    return report


async def create_sport_report(report: SportsEventSchema) -> SportsEventSchema:
    """
    Creates a new sports event report in the database from the provided SportsEventSchema.

    Args:
        report (SportsEventSchema): The sports event data to be stored.

    Returns:
        SportsEventSchema: The original sports event schema that was passed in.
    """
    print(report.model_dump())
    sports_event = SportsEventReport(**report.model_dump())
    await sports_event.insert()
    return report


async def get_sport_by_event(event_name: str) -> Optional[SportsEventReport]:
    """
    Retrieves a sports event report by its event name.

    Args:
        event_name (str): The name of the sports event.

    Returns:
        Optional[SportsEventReport]: The sports event report if found, otherwise None.
    """
    sports_event = await SportsEventReport.find_one(SportsEventReport.event_name == event_name)
    return sports_event


async def get_all_sports() -> List[SportsEventReport]:
    """
    Retrieves all sports event reports.

    Returns:
        List[SportsEventReport]: A list of all sports event reports in the database.
    """
    reports = await SportsEventReport.find_all().to_list()
    return reports


async def update_sport_report(report: SportsEventSchema) -> SportsEventReport:
    """
    Updates an existing sports event report with new data.

    Args:
        report (SportsEventSchema): The updated data for the sports event.

    Returns:
        SportsEventReport: The updated sports event report.
    """
    to_update = await SportsEventReport.find_one(SportsEventReport.event_name == report.event_name)
    await to_update.set({
        SportsEventReport.commence_time: report.commence_time,
        SportsEventReport.sport_title: report.sport_title,
        SportsEventReport.home_team: report.home_team,
        SportsEventReport.away_team: report.away_team
    })
    return to_update


async def delete_sport_report(event_name: str) -> bool:
    """
    Deletes a sports event report by its event name.

    Args:
        event_name (str): The name of the sports event to delete.

    Returns:
        bool: True if the report was deleted, False otherwise.
    """
    to_delete = await SportsEventReport.find_one(SportsEventReport.event_name == event_name)
    if to_delete:
        await to_delete.delete()
        return True
    return False


async def get_by_city(city: str) -> Optional[WeatherReport]:
    """
    Retrieves a weather report by city name.

    Args:
        city (str): The name of the city.

    Returns:
        Optional[WeatherReport]: The weather report for the specified city, or None if not found.
    """
    weather_report = await WeatherReport.find_one(WeatherReport.city == city)
    return weather_report


async def get_all() -> List:
    """
    Retrieves all weather reports.

    Returns:
        List[WeatherReport]: A list of all weather reports in the database.
    """
    reports = await WeatherReport.find_all().to_list()
    return reports


async def update(report: WeatherSchema) -> WeatherReport:
    """
    Updates an existing weather report with new data based on the provided WeatherSchema.

    Args:
        report (WeatherSchema): The updated weather data.

    Returns:
        WeatherReport: The updated weather report.
    """
    to_update = await WeatherReport.find_one(WeatherReport.city == report.city)
    await to_update.set({
        WeatherReport.temperature: report.temperature,
        WeatherReport.humidity: report.humidity,
        WeatherReport.wind_speed: report.wind_speed,
        WeatherReport.time: report.time
    })
    return to_update


async def delete(city: str) -> bool:
    """
    Deletes a weather report by city name.

    Args:
        city (str): The name of the city whose report should be deleted.

    Returns:
        bool: True if the report was deleted, False otherwise.
    """
    to_delete = await WeatherReport.find_one(WeatherReport.city == city)
    if to_delete:
        await to_delete.delete()
        return True
    return False

