from motor import motor_asyncio

from backend.config import MONGODB_URL


client = motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
