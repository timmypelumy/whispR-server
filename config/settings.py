from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):

    """ Application Settings """

    app_name:  str = "whispR"
    debug:  bool = True
    allowed_origins: list = ["localhost:7000", "localhost:3000"]
    exposed_headers: list = []
    password_salt: str = "whispRSalt"
    db_url: str = "mongodb://localhost:4000"
    db_name:  str = "whispR"
    jwt_exp_hours: int = 24
    jwt_secret: str = "whispRSecret"
    jwt_algorithm: str = "HS256"
    mail_username: str = "whispR"
    mail_password: str = "mail_pass"
    mail_from: str = "whispRteam@whispR.com"
    mail_port: int = 587
    mail_server:  str = "https://mail.com"
    mail_starttls: bool = False
    mail_ssl_tls:  bool = True
    mail_display_name: str = "whispR"
    mail_domain:  str = "https://mail.com"
    mail_domain_username:  str = "admin"
    encryption_key1: str = "whispRKey1"
    encryption_key2: str = "whispRKey2"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    return Settings()
