import httpx
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from backend.models.sports_models import EventScoresScheme, ScoresScheme
# from backend.config import API_KEY
from backend.config import Config

config = Config()

SPORT_SCORE_URL = "https://api.the-odds-api.com/v4/sports/{sport}/scores/?apiKey={apiKey}&daysFrom={daysFrom}&dateFormat={dateFormat}"
scores_router = APIRouter(include_in_schema=True)

class SportDataAdapter:
    @staticmethod
    def adapt_event_score(data, sport: str, team: Optional[str] = None) -> List[EventScoresScheme]:
        sports_data = []
        for game in data:
            if game.get("sport_key") == sport and (team is None or team in [game.get("home_team"), game.get("away_team")]):
                scores = []
                if game.get("scores"):
                    for team_score in game["scores"]:
                        scores.append(ScoresScheme(name=team_score.get('name', ''), score=[team_score.get('score', 0)]))
                
                sports_data.append(EventScoresScheme(
                    sport_key=game.get('sport_key', ''),
                    sport_title=game.get('sport_title', ''),
                    commence_time=game.get('commence_time', ''),
                    completed=game.get('completed', False),
                    home_team=game.get('home_team', ''),
                    away_team=game.get('away_team', ''),
                    score=scores
                ))

        return sports_data
                

@scores_router.get('/sports/{sport}/scores', response_model=List[EventScoresScheme])
async def get_event_scores_by_sport_key(
    sport: str,
    days_from: Optional[int] = Query(3, description="Number of days in the past to include completed games (1-3)"),
    date_format: Optional[str] = Query("iso", description="Format for timestamps (unix or iso)")
):
    url = SPORT_SCORE_URL.format(sport=sport, apiKey=config.API_KEY, daysFrom=days_from, dateFormat=date_format)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail="Failed to fetch sports data")
        
    data = response.json()

    if not data:
        raise HTTPException(status_code=404, detail="No data found for the specified sport")

    sports_data = SportDataAdapter.adapt_event_score(data, sport=sport)

    if not sports_data:
        raise HTTPException(status_code=404, detail="No data found for the specified sport")

    return sports_data

@scores_router.get('/sports/{sport}/teams/{team}/scores', response_model=List[EventScoresScheme])
async def get_event_scores_by_sport_and_team(
    sport: str,
    team: str,
    days_from: Optional[int] = Query(3, description="Number of days in the past to include completed games (1-3)"),
    date_format: Optional[str] = Query("iso", description="Format for timestamps (unix or iso)")
):
    url = SPORT_SCORE_URL.format(sport=sport, apiKey=config.API_KEY, daysFrom=days_from, dateFormat=date_format)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail="Failed to fetch sports data")
        
    data = response.json()

    if not data:
        raise HTTPException(status_code=404, detail="No data found for the specified sport")

    sports_data = SportDataAdapter.adapt_event_score(data, sport=sport, team=team)
    
    if not sports_data:
        raise HTTPException(status_code=404, detail="No data found for the specified team")

    return sports_data
