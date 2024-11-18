from urllib.parse import urlencode

from backend.config import WEATHER_API_KEY


def build_weather_query(base_url: str, city: str, imperial=False) -> str:
    """Builds the URL for an API request to OpenWeather's weather API.

    Args:
        base_url (str): base url to request
        city (str): Name of a city as collected by argparse
        imperial (bool): Use or not imperial units for temperature

    Returns:
        str: URL formatted for a call to OpenWeather's city name endpoint
    """
    units = "imperial" if imperial else "metric"
    request_data = {'q': city,
                    'appid': WEATHER_API_KEY,
                    'units': units}
    url_values = urlencode(request_data)
    full_url = base_url + '?' + url_values
    return full_url
