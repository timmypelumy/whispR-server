from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):

    """ Application Settings """

    app_name :  str  = "whispR"
    debug  :  bool = True
    allowed_origins : list = ["localhost:7000", "localhost:3000"]
    exposed_headers : list = []
    password_salt : str = "whispRSalt"
    db_url : str = "mongodb://localhost:4000"
    db_name :  str = "whispR"


    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    return Settings()