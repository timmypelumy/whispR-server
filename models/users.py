from pydantic import BaseModel, Field, EmailStr, validator
from pydantic_settings import SettingsConfigDict
from utils.pure_functions import *
from utils.security import verify_password, create_jwt_token, decode_jwt_token


USER_EXCLUDE_FIELDS = ["password_hash"]


class AccessToken(BaseModel):
    """ Access Token Model """

    access_token: str = Field(alias="accessToken")
    token_type: str = Field(alias="tokenType")

    model_config = SettingsConfigDict(populate_by_name=True)


class BaseUser(BaseModel):
    """ Base User Model """

    username: str = Field(min_length=3, max_length=20)
    email: EmailStr

    model_config = SettingsConfigDict(populate_by_name=True)

    @validator("username")
    def username_validator(cls, v):
        if v.isnumeric():
            raise ValueError("Username cannot be numeric")

        if not v.isidentifier():
            raise ValueError("Username must be alphanumeric")

        return v

    @validator("email")
    def email_validator(cls, v):
        return v.lower()


class UserIn(BaseUser):

    """  UserIn Model """

    password: str = Field(min_length=8, max_length=25)
    model_config = SettingsConfigDict(populate_by_name=True)


class User(BaseUser):
    """ User Model """
    uid: str = Field(default_factory=get_uuid, alias="uid")
    is_active: bool = Field(default=True, alias="isActive")
    is_admin: bool = Field(default=False, alias="isAdmin")
    password_hash: str = Field(alias="passwordHash")
    created_at: float = Field(
        default_factory=get_utc_timestamp, alias="createdAt")
    updated_at: float | None = Field(default=None, alias="updatedAt")

    def check_password(self, password: str) -> bool:
        """ Checks if the password is valid """

        return verify_password(password, self.password_hash)

    def create_jwt_token(self, payload) -> str:
        """ Creates a JWT token """

        return create_jwt_token(payload)

    def decode_jwt_token(self, token: str) -> dict:
        """ Decodes a JWT token """

        return decode_jwt_token(token)

    model_config = SettingsConfigDict(populate_by_name=True)
