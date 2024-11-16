from typing import List, Optional
from backend.models.sports_models import SportReport, SportScheme, ScoreReport, EventScoresScheme, ScoresScheme

async def create_sport_report(sport_data: SportScheme) -> SportReport:
    sport_report = SportReport(**sport_data.model_dump())
    await sport_report.insert()
    return sport_report

async def get_sport_report_by_key(key: str) -> Optional[SportReport]:
    sport_report = await SportReport.get_sport_by_key(key)  
    return sport_report

async def get_all_sport_reports() -> List[SportReport]:
    return await SportReport.find_all().to_list() 

async def update_sport_report(report_id: str, updated_data: SportScheme) -> Optional[SportReport]:
    sport_report = await SportReport.get(report_id)  
    if sport_report:
        sport_report.key = updated_data.key
        sport_report.group = updated_data.group
        sport_report.title = updated_data.title
        sport_report.description = updated_data.description
        sport_report.active = updated_data.active
        sport_report.has_outrights = updated_data.has_outrights
        await sport_report.save() 
        return sport_report
    return None 

async def delete_sport_report(report_id: str) -> Optional[SportReport]:
    sport_report = await SportReport.get(report_id)  
    if sport_report:
        await sport_report.delete()  
        return sport_report 
    return None 


async def get_scores_report_by_key(sport_key: str) -> Optional[ScoreReport]:
    scores_report = await ScoreReport.get_event_by_id(sport_key)
    return scores_report

async def update_event_scores(event_id: str, updated_scores: EventScoresScheme) -> Optional[EventScoresScheme]:
    event_scores = await ScoreReport.get_event_by_id(event_id)
    
    if event_scores:
        event_scores.sport_key = updated_scores.sport_key
        event_scores.sport_title = updated_scores.sport_title
        event_scores.commence_time = updated_scores.commence_time
        event_scores.completed = updated_scores.completed
        event_scores.home_team = updated_scores.home_team
        event_scores.away_team = updated_scores.away_team
        event_scores.score = [
            ScoresScheme(name=score.name, score=score.score) for score in updated_scores.score
        ]
        
        await event_scores.save()
        return event_scores 
    return None
