# events/services.py
import requests
from .singleton import APIClientSingleton
from .models import FootballEvent

class FootballEventFacade:
    def __init__(self):
        self.api_client = APIClientSingleton()  # Використовуємо Одинак

    def fetch_events(self):
        """Отримуємо дані з API"""
        response = requests.get(self.api_client.url, headers=self.api_client.headers)
        return response.json().get("events", [])
    
    def save_events(self, events_data):
        """Зберігаємо дані в базі"""
        for event_data in events_data:
            FootballEvent.objects.update_or_create(
                event_id=event_data["id"],
                defaults={
                    "tournament": event_data["tournament"].get("name", "N/A"),
                    "home_team": event_data["homeTeam"]["name"],
                    "away_team": event_data["awayTeam"]["name"],
                    "home_score": event_data.get("homeScore", {}).get("current", 0),
                    "away_score": event_data.get("awayScore", {}).get("current", 0),
                    "start_timestamp": event_data["startTimestamp"],
                    "slug": event_data["slug"],
                }
            )
    
    def fetch_and_save_events(self):
        """Комбінована функція для отримання та збереження даних"""
        events_data = self.fetch_events()
        self.save_events(events_data)
