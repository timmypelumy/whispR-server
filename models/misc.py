from pydantic import BaseModel, Field
from utils.pure_functions import get_utc_timestamp, get_uuid


class TwoFactor(BaseModel):
    """ Two Factor Model """

    uid: str = Field(default_factory=get_uuid)
    secret: str
    otp: str
    is_active: bool
    created_at: float = Field(default_factory=get_utc_timestamp)
    updated_at: float | None
