import os  # Import the os module for accessing environment variables
from dotenv import load_dotenv  # Import load_dotenv from dotenv to load environment variables from a .env file

# Load environment variables from a .env file into the environment
load_dotenv()

# Fetch API keys and database credentials from environment variables
SPORT_API_KEY = os.getenv("SPORT_API_KEY")  # API key for the sports service
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # API key for the weather service

# MongoDB credentials and connection details
MONGODB_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")  # MongoDB root username
MONGODB_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")  # MongoDB root password
MONGO_DATABASE = os.getenv("MONGO_INITDB_DATABASE")  # Name of the MongoDB database to use
MONGODB_PORT = os.getenv("MONGODB_PORT")  # MongoDB service port (typically 27017)
MONGODB_HOST = os.getenv("MONGODB_HOST")  # MongoDB service host (typically "localhost" or a container address)

# Construct the MongoDB URL using the environment variables
MONGODB_URL = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGO_DATABASE}" \
              f"?authSource=admin"  # Construct the URL to connect to MongoDB with authentication