import uuid
import datetime
import secrets


def get_uuid():
    return str(uuid.uuid4())


def get_uuid1():
    return str(uuid.uuid1())


def get_utc_timestamp():
    return datetime.datetime.utcnow().timestamp()


def get_token():
    return secrets.token_urlsafe(32)
