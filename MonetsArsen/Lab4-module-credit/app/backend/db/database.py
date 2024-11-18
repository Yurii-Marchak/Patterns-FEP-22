from motor import motor_asyncio  # Import the async MongoDB client from Motor (asynchronous MongoDB driver)

from backend.config import MONGODB_URL  # Import the MongoDB connection URL from the configuration

# Create an instance of AsyncIOMotorClient, which connects to the MongoDB database asynchronously.
# This client will be used to interact with the MongoDB database specified by MONGODB_URL.
client = motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
