# Weather and Sports API

This project provides a RESTful API for fetching current weather, weather forecasts, air pollution data, and sports events. The API retrieves data from external APIs such as OpenWeather and others, and stores the information in a MongoDB database.

## Tech Stack

- **FastAPI**: A modern Python framework for building APIs.
- **MongoDB**: A NoSQL database for storing weather reports and sports event data.
- **Motor**: Async driver for MongoDB used to interact with the database asynchronously.
- **httpx**: A library for making asynchronous HTTP requests.
- **Pydantic**: For data validation and serialization.
- **pytest**: For testing asynchronous functions.

## Installation

1. Clone the repository:  
   `git clone https://github.com/your-repo.git`  
   `cd your-repo`

2. Create a virtual environment:  
   `python3 -m venv venv`  
   `source venv/bin/activate`  # for Unix/macOS  
   `venv\Scripts\activate`  # for Windows

3. Install the dependencies:  
   `pip install -r requirements.txt`

4. Set up environment variables:

5. Create a `.env` file at the root of the project and add the following variables:
SPORT_API_KEY=your_sport_api_key WEATHER_API_KEY=your_weather_api_key MONGODB_USERNAME=your_mongodb_username MONGODB_PASSWORD=your_mongodb_password MONGO_DATABASE=your_mongo_database MONGODB_PORT=your_mongodb_port MONGODB_HOST=your_mongodb_host
## Running the Project

1. Start the application:  
`uvicorn backend.main:app --reload`

2. Go to [http://localhost:8000/docs](http://localhost:8000/docs) to view the auto-generated API documentation using Swagger.

## Endpoints

### Weather

- **GET** `/current/`  
Fetches current weather for a specified city.  
Parameters:  
- `city` (str): The name of the city.  
- `imperial` (bool): Whether to use imperial units for temperature (default is False).

- **POST** `/current`  
Creates a new weather report.  
Request body example:  
```json  
{  
 "city": "Kyiv",  
 "coordinates": [50.4501, 30.5236],  
 "description": "clear sky",  
 "temperature": 15.0,  
 "humidity": 60,  
 "wind_speed": 5.0,  
 "time": "2024-11-18T12:00:00"  
}
```

- **GET** `/current/{city}`
Fetches the weather report for a specified city.

- **GET** `/current/all/`
Retrieves all weather reports stored in the database.

- **PUT** `/current/`
Updates an existing weather report for a specified city.

- **POST** `/current/from_another_api`
Creates a new weather report from OpenWeather API.

Sports
- **GET** `/sport/`
Fetches all sports events.
Returns a list of sports events stored in the database.

- **GET** `/sport/scores`
Fetches sports scores for a specific sport.
Parameters:
- sport (str): The name of the sport (e.g., "football", "basketball").

- **POST** `/sport/`
Creates a new sports event.
Request body example:
```json  
{
  "event_name": "Championship Final",
  "sport_title": "Soccer",
  "commence_time": "2024-11-04T15:00:00",
  "home_team": "Team A",
  "away_team": "Team B"
}
```

- **GET** `/sport/{event_name}`
Fetches a sports event by its name.

- **PUT** `/sport/`
Updates an existing sports event.
Request body example:
```json  
{
  "event_name": "Championship Final",
  "sport_title": "Soccer",
  "commence_time": "2024-11-04T16:00:00",
  "home_team": "Team A",
  "away_team": "Team C"
}
```

- **DELETE** `/sport/{event_name}`
Deletes a sports event by its name.

### Explanation of Sports Endpoints:
1. **GET** `/sport/` - Fetches all stored sports events from the database.
2. **GET** `/sport/scores` - Retrieves sports scores for a specific sport (e.g., football, basketball) by providing the sport name.
3. **POST** `/sport/` - Creates a new sports event, where you provide the event's name, sport, teams, and the time of commencement.
4. **GET** `/sport/{event_name}` - Retrieves details of a specific sports event by its name.
5. **PUT** `/sport/` - Updates an existing sports event based on the event's name.
6. **DELETE** `/sport/{event_name}` - Deletes a specific sports event by its name.