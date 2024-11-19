# events/singleton.py
from football_events import settings


class APIClientSingleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(APIClientSingleton, cls).__new__(cls)
            # Ініціалізація налаштувань API
            cls._instance.url = "https://sportapi7.p.rapidapi.com/api/v1/sport/football/scheduled-events/2022-02-11"
            cls._instance.headers = {
                "x-rapidapi-key": settings.RAPIDAPI_KEY,
                "x-rapidapi-host": settings.RAPIDAPI_HOST,
                "Accept": "application/json"
            }
        return cls._instance
