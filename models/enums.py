from enum import Enum


class PKTypes(str, Enum):
    EMAIL = "email"
    USERNAME = "username"
    UID = "uid"
