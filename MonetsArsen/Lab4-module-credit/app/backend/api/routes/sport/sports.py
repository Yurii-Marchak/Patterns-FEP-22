from http.client import HTTPException
from typing import List

import httpx
from fastapi import APIRouter
from urllib.parse import urlencode

from backend.config import SPORT_API_KEY
from backend.db.crud import get_all_sports, create_sport_report, get_sport_by_event, update_sport_report, \
    delete_sport_report
from backend.models.sport_event import SportsEventSchema, SportsEventAdapter

sport_router = APIRouter(include_in_schema=True)

SPORT_API_URL = "https://api.the-odds-api.com/v4/sports/"

@sport_router.get("/sport/")
async def get_sports():
    """
    Retrieve available sports from the odds API.

    Returns:
        dict: List of available sports and their details.
    """
    request_data = {'apiKey': SPORT_API_KEY}
    url_values = urlencode(request_data)
    url = SPORT_API_URL + "?" + url_values
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        sport_info = response.json()
    return sport_info

@sport_router.get("/sport/odds")
async def get_sports_odds(sport: str, region: str):
    """
    Fetch sports odds for a specific sport and region.

    Args:
        sport (str): Sport identifier
        region (str): Geographic region for odds

    Returns:
        dict: Detailed sports odds information
    """
    request_data = {'apiKey': SPORT_API_KEY,
                    'regions': region}
    url_values = urlencode(request_data)
    url = SPORT_API_URL + sport + "/odds/?" + url_values
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        sport_info = response.json()
    return sport_info

@sport_router.get("/sport/scores")
async def get_sports_scores(sport: str):
    """
       Retrieve scores for a specific sport.

       Args:
           sport (str): Sport identifier

       Returns:
           dict: Current sports scores
       """
    request_data = {'apiKey': SPORT_API_KEY}
    url_values = urlencode(request_data)
    url = SPORT_API_URL + sport + "/scores/?" + url_values
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        sport_info = response.json()
    return sport_info

@sport_router.get("/sport/events")
async def get_sports_events(sport: str):
    """
            Get upcoming events for a specific sport.

            Args:
                sport (str): Sport identifier

            Returns:
                dict: List of sporting events
            """
    request_data = {'apiKey': SPORT_API_KEY}
    url_values = urlencode(request_data)
    url = SPORT_API_URL + sport + "/events/?" + url_values
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        sport_info = response.json()
    return sport_info

@sport_router.post("/sport/", response_model=SportsEventSchema)
async def create_sport_event(report: SportsEventSchema):
    """
       Create a new sports event report.

       Args:
           report (SportsEventSchema): Sports event details

       Returns:
           SportsEventSchema: Created sports event
       """
    return await create_sport_report(report)

@sport_router.get("/sport/all/", response_model=List[SportsEventSchema])
async def get_all_sports_reports():
    """
       Retrieve all stored sports event reports.

       Raises:
           HTTPException: If no sports reports are found

       Returns:
           List[SportsEventSchema]: All sports event reports
       """
    sports_reports = await get_all_sports()
    if not sports_reports:
        raise HTTPException(404, "No sports reports found.")
    return sports_reports

@sport_router.get("/sport/{event_name}/", response_model=SportsEventSchema)
async def get_sport_event(event_name: str):
    """
    Fetch a specific sports event by its name.

    Args:
        event_name (str): Unique identifier for the sports event

    Raises:
        HTTPException: If the sports event is not found

    Returns:
        SportsEventSchema: Detailed sports event information
    """
    sports_event = await get_sport_by_event(event_name)
    if not sports_event:
        raise HTTPException(404, "Sports event not found.")
    return sports_event

@sport_router.put("/sport/", response_model=SportsEventSchema)
async def update_sport_event(report: SportsEventSchema):
    """
       Update an existing sports event report.

       Args:
           report (SportsEventSchema): Updated sports event details

       Raises:
           HTTPException: If update fails

       Returns:
           SportsEventSchema: Updated sports event
       """
    sports_event = await update_sport_report(report)
    if not sports_event:
        raise HTTPException(404, "There was an error updating the sports event.")
    return sports_event

@sport_router.delete("/sport/delete/", response_model=bool)
async def delete_sport_event(event_name: str):
    """
        Delete a sports event report.

        Args:
            event_name (str): Unique identifier for the sports event

        Raises:
            HTTPException: If deletion fails

        Returns:
            bool: Success status of deletion
        """
    result = await delete_sport_report(event_name)
    if not result:
        raise HTTPException(404, "There was an error deleting the sports event.")
    return result

@sport_router.post("/sport/from_another_api", response_model=List [SportsEventSchema])
async def create_sport_report_from_another_api(sport: str):
    """
    Create sports event reports by fetching data from an external API.

    Args:
        sport (str): Sport identifier

    Raises:
        HTTPException: If the sports event already exists

    Returns:
        List[SportsEventSchema]: Newly created sports event reports
    """
    # Check if the sports event already exists
    sports_event = await get_sport_by_event(sport)
    if sports_event is not None:
        raise HTTPException(409, "The sports event already exists")

    request_data = {'apiKey': SPORT_API_KEY}
    url_values = urlencode(request_data)
    url = SPORT_API_URL + sport + "/events/?" + url_values
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        sports_info = response.json()

    sports_reports = []
    for sport_info in sports_info:
        sports_data = SportsEventAdapter(sport_info)
        created_sport_report = await create_sport_report(report=sports_data)
        sports_reports.append(created_sport_report)

    return sports_reports

