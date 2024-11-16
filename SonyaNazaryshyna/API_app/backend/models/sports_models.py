from datetime import datetime
from typing import List
from beanie import Document
from pydantic import BaseModel, Field


class SportScheme(BaseModel):
    key: str
    group: str
    title: str
    description: str  
    active: bool  
    has_outrights: bool  
    
class SportReport(Document, SportScheme):
    def __repr__(self) -> str:
        return f"<SportReport {self.title} ({self.key})>"

    def __str__(self) -> str:
        return f"{self.title} ({self.key})"

    def __hash__(self) -> int:
        return hash((self.key, self.group))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SportReport):
            return (self.key, self.group) == (other.key, other.group)
        return False

    @classmethod
    async def get_sport_by_key(cls, key: str) -> "SportReport":
        return await cls.find_one({"key": key})

    @classmethod
    async def get_sports_by_group(cls, group: str) -> List["SportReport"]:
        return await cls.find({"group": group}).to_list()

    @classmethod
    async def active_sports(cls) -> List["SportReport"]:
        return await cls.find({"active": True}).to_list()
    
    @classmethod
    async def delete_sport_report(cls, key: str) -> bool:
        sport_report = await cls.find_one({"key": key})
        if sport_report:
            await sport_report.delete()
            return True
        return False


class ScoresScheme(BaseModel):
    name: str
    score: List[str]

class EventScoresScheme(BaseModel):
    sport_key: str
    sport_title: str
    commence_time: datetime
    completed: bool
    home_team: str
    away_team: str
    score: List[ScoresScheme] = Field(default_factory=list)

class ScoreReport(Document, EventScoresScheme):
    def __repr__(self) -> str:
        return f"<ScoreReport {self.home_team} vs {self.away_team} ({self.id})>"

    def __str__(self) -> str:
        return f"{self.home_team} vs {self.away_team} ({self.id})"

    @classmethod
    async def get_event_by_id(cls, event_id: str) -> "ScoreReport":
        event = await cls.find_one({"id": event_id})
        return event

    @classmethod
    async def get_all_events(cls) -> List["ScoreReport"]:
        return await cls.find().to_list()

__beanie_models__ = [SportReport, ScoreReport]