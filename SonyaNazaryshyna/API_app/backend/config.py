# import os
# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.getenv("API_KEY")
# MONGODB_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
# MONGODB_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
# MONGO_DATABASE = os.getenv("MONGO_INITDB_DATABASE")
# MONGODB_PORT = os.getenv("MONGODB_PORT")
# MONGODB_HOST = os.getenv("MONGODB_HOST")
# MONGODB_URL = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGO_DATABASE}" \
#               f"?authSource=admin"

import os
from dotenv import load_dotenv

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            load_dotenv()
            cls._instance.API_KEY = os.getenv("API_KEY")
            cls._instance.MONGODB_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
            cls._instance.MONGODB_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
            cls._instance.MONGO_DATABASE = os.getenv("MONGO_INITDB_DATABASE")
            cls._instance.MONGODB_PORT = os.getenv("MONGODB_PORT")
            cls._instance.MONGODB_HOST = os.getenv("MONGODB_HOST")
            if None in (cls._instance.MONGODB_USERNAME, cls._instance.MONGODB_PASSWORD,
                         cls._instance.MONGO_DATABASE, cls._instance.MONGODB_PORT,
                         cls._instance.MONGODB_HOST):
                raise EnvironmentError("One or more environment variables are missing.")

            cls._instance.MONGODB_URL = f"mongodb://{cls._instance.MONGODB_USERNAME}:{cls._instance.MONGODB_PASSWORD}@" \
                                         f"{cls._instance.MONGODB_HOST}:{cls._instance.MONGODB_PORT}/{cls._instance.MONGO_DATABASE}" \
                                         "?authSource=admin"
        return cls._instance
config = Config()
print(config.MONGODB_URL)
