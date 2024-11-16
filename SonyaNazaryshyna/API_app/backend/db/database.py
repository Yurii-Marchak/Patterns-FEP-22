from motor import motor_asyncio
from backend.config import Config

config = Config()

client = motor_asyncio.AsyncIOMotorClient(config.MONGODB_URL)