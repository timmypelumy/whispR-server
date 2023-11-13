from pydantic import BaseModel, Field
from utils.pure_functions import get_utc_timestamp, get_uuid, get_token


class OTP(BaseModel):
    """ Two Factor Model """

    uid: str = Field(default_factory=get_uuid)
    token: str = Field(default_factory=get_token)
    foreign_id: str
    secret: str
    action: str
    is_active: bool
    created_at: float = Field(default_factory=get_utc_timestamp)
    updated_at: float | None = Field(default=None)
