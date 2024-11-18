from datetime import datetime
from unittest.mock import patch

import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from backend.api.routes import sport_router
from backend.models.sport_event import SportsEventSchema

app = FastAPI()
app.include_router(sport_router)

@pytest.mark.asyncio
async def test_get_sports():
    """
    Test to ensure that the '/sport/' endpoint returns a successful response.

    This test sends a GET request to the '/sport/' endpoint and asserts that the
    status code of the response is 200, indicating a successful request.
    """
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get("/sport/")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_sports_scores_unknown_sport():
    """
    Test to check the behavior when querying scores for an unknown sport.

    This test sends a GET request to the '/sport/scores' endpoint with the sport
    parameter set to 'football', which is expected to return an error response
    indicating that the sport is unknown.
    """
    response_data = {
        "message": "Unknown sport",
        "error_code": "UNKNOWN_SPORT",
        "details_url": "https://the-odds-api.com/liveapi/guides/v4/api-error-codes.html#unknown-sport"
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get("/sport/scores?sport=football")

    assert response.status_code == 200
    assert response.json() == response_data

@pytest.mark.asyncio
@patch('backend.api.routes.sport.sports.create_sport_report')  # Adjust the path as necessary
async def test_create_sport_event(mock_create_sport_report):
    """
    Test the creation of a new sports event via the '/sport/' endpoint.

    This test mocks the call to create a sports event report. It checks that
    when a POST request with the event data is made, the response returns the
    correct data and verifies that the mock create_sport_report function is called
    with the correct parameters.

    Args:
        mock_create_sport_report (MagicMock): The mock function to replace the
        actual `create_sport_report` function in the route handler.
    """
    # Define the mock input data
    mock_event_data = {
        "event_name": "Championship Final",
        "sport_title": "Soccer",
        "commence_time": datetime(2024, 11, 4, 15, 0, 0).isoformat(),
        "home_team": "Team A",
        "away_team": "Team B"
    }
    mock_event = SportsEventSchema(**mock_event_data)

    # Set the return value of the mock
    mock_create_sport_report.return_value = mock_event

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post("/sport/", json=mock_event_data)

    # Check the response
    assert response.status_code == 200
    assert response.json() == mock_event_data
    mock_create_sport_report.assert_called_once_with(mock_event)
