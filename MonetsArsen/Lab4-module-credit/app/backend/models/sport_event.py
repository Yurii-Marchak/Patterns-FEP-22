from datetime import datetime
from beanie import Document
from pydantic import BaseModel


class SportsEventSchema(BaseModel):
    """
    Pydantic schema representing a sports event with core attributes.

    Attributes:
        event_name (str): Name or identifier of the sports event.
        sport_title (str): Type or category of sport.
        commence_time (datetime): Scheduled start time of the event.
        home_team (str): Name of the team hosting the event.
        away_team (str): Name of the opposing team.
    """
    event_name: str
    sport_title: str
    commence_time: datetime
    home_team: str
    away_team: str


class SportsEventReport(Document, SportsEventSchema):
    """
    Beanie document representing a sports event with additional representations.

    Extends SportsEventSchema to provide custom string representations
    and a property for document creation time.
    """
    def __repr__(self) -> str:
        """
        Creates a detailed string representation of the sports event.

        Returns:
            str: Formatted representation showing sport and teams.
        """
        return f"<SportsEventReport {self.sport_title}: {self.home_team} vs {self.away_team}>"

    def __str__(self) -> str:
        """
        Creates a concise string representation of the sports event.

        Returns:
            str: Matchup between home and away teams.
        """
        return f"{self.home_team} vs {self.away_team}"

    @property
    def created(self) -> datetime:
        """
        Retrieves the datetime when the sports event report was created.

        Returns:
            datetime: Generation time of the document's ID.
        """
        return self.id.generation_time


class SportsEventAdapter(SportsEventReport):
    """
    Adapter for creating sports event reports from JSON input.

    Provides a flexible initialization method that auto-generates
    event names and ensures data consistency.
    """
    def __init__(self, json: dict):
        """
        Initializes a sports event report from a JSON dictionary.

        Args:
            json (dict): Input dictionary containing sports event details.
                Expected keys: 'sport_title', 'commence_time',
                'home_team', 'away_team'

        Note:
            Automatically generates a composite event name from input data.
        """
        # Ensure the required fields are present
        json_data = {
            "event_name":  f"{json['home_team']} - {json['away_team']} | {json['sport_title']}",
            "sport_title": json['sport_title'],
            "commence_time": json['commence_time'],
            "home_team": json['home_team'],
            "away_team": json['away_team']
        }
        # Call the superclass initializer with unpacked data
        super().__init__(**json_data)