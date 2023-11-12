from motor import motor_asyncio
from enum import Enum
from config.settings import get_settings

settings = get_settings()


class COLS(str, Enum):
    USERS = "users"
    OTPS = "otps"


client = motor_asyncio.AsyncIOMotorClient(settings.db_url)


DB = client[settings.db_name]
