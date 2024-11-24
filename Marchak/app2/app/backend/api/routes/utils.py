from urllib.parse import urlencode
from backend.config import SPORTS_API_KEY

def build_sports_query(base_url: str, params: dict) -> str:
    """Builds the URL for an API request to a sports API.

    Args:
        base_url (str): Base URL of the API.
        params (dict): Query parameters for the API request.

    Returns:
        str: URL formatted for the API call.
    """
    params['apikey'] = SPORTS_API_KEY
    url_values = urlencode(params)
    return f"{base_url}?{url_values}"
