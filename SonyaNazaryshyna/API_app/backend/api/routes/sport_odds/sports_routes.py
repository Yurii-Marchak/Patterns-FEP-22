import httpx
from fastapi import APIRouter, HTTPException, Query
from typing import List

from backend.db.crud import *
# from backend.config import API_KEY
from backend.config import Config

config = Config()

SPORTS_API_URL = f"https://api.the-odds-api.com/v4/sports/?apiKey={config.API_KEY}"
sports_router = APIRouter(include_in_schema=True)

@sports_router.get('/sports/{key}', response_model=SportScheme)
async def get_sport_by_key(key: str):
    local_sport = await get_sport_report_by_key(key)
    if local_sport:
        return local_sport
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(SPORTS_API_URL)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail="Failed to fetch sports data")

    sports_data = response.json()
    sport = next((sport for sport in sports_data if sport.get("key") == key), None)
    
    if sport is None:
        raise HTTPException(status_code=404, detail="Sport not found")
    
    return sport


@sports_router.get('/sports/{group}/group', response_model=List[SportScheme])
async def get_sports_by_group(group: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(SPORTS_API_URL)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail="Failed to fetch sports data by group")
        
    sports_data_by_group = response.json()
    sports_data_by_group = [sport for sport in sports_data_by_group if sport.get("group") == group]
    
    if not sports_data_by_group:
        raise HTTPException(status_code=404, detail="No sports found in this group")
        
    return sports_data_by_group

@sports_router.post('/sports', response_model=SportScheme)
async def create_sports_report(report: SportScheme):
    existing_report = await get_sport_report_by_key(report.key)
    if existing_report is not None:
        raise HTTPException(status_code=409, detail="The sports already exists")

    sport_report = await create_sport_report(report)

    print(f"Created sport report: {sport_report}")
    
    return sport_report

@sports_router.delete('/sports/{key}', response_model=SportScheme)
async def delete_sports(key: str):
    sport_report = await get_sport_report_by_key(key)
    
    if sport_report is None:
        raise HTTPException(status_code=404, detail="Sport report not found")
    
    delete_success = await SportReport.delete_sport_report(key)
    
    if not delete_success:
        raise HTTPException(status_code=500, detail="Failed to delete the sport report")
    
    return sport_report

@sports_router.put('/sports/{key}', response_model=SportScheme)
async def update_sport(key: str, sport_data: SportScheme):
    sport_report = await SportReport.get_sport_by_key(key)
    if not sport_report:
        raise HTTPException(status_code=404, detail="Sport not found")
    
    for attr, value in sport_data.dict().items():
        setattr(sport_report, attr, value)
    
    await sport_report.save()
    return sport_report