from enum import Enum


class PKTypes(str, Enum):
    EMAIL = "email"
    USERNAME = "username"
    UID = "uid"


class Actions(str, Enum):
    VERIFY_EMAIL = "verify_email"
    RESET_PASSWORD = "reset_password"
    CHANGE_PASSWORD = "change_password"
    CHANGE_EMAIL = "change_email"
    CHANGE_USERNAME = "change_username"
    CHANGE_TFA = "change_tfa"
    DELETE_ACCOUNT = "delete_account"


class Emails(str, Enum):
    VERIFY_EMAIL = "verify_email"
    RESET_PASSWORD = "reset_password"
    CHANGE_EMAIL = "change_email"
    CHANGE_USERNAME = "change_username"
    CHANGE_TFA = "change_tfa"
    DELETE_ACCOUNT = "delete_account"
    ACCOUNT_DELETED = "account_deleted"
