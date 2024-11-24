import httpx
from fastapi import APIRouter, HTTPException

from backend.api.routes.utils import build_sports_query

sports_router = APIRouter()

SPORTS_API_URL = "https://www.thesportsdb.com/api/v1/json"

@sports_router.get("/matches/")
async def get_matches(league: str, season: str):
    """Fetches matches for a given league and season.

    Args:
        league (str): League ID.
        season (str): Season year.

    Returns:
        dict: Match details.
    """
    url = build_sports_query(base_url=f"{SPORTS_API_URL}/1/eventsseason.php", params={"id": league, "s": season})
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching data")
        return response.json()
