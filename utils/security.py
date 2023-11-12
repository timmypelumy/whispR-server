from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.twofactor.totp import HOTP
from cryptography.fernet import MultiFernet, Fernet
from cryptography.hazmat.primitives.hashes import SHA1, SHA256, Hash
from cryptography.exceptions import InvalidKey
from config.settings import get_settings
from base64 import b64encode, b64decode
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from models.misc import OTP
from utils.db import COLS, DB
import jwt
import os
import binascii


settings = get_settings()


def encode_base64(data: bytes) -> str:
    """ Encodes bytes to base64 """

    return b64encode(data).decode()


def decode_base64(data: str) -> bytes:
    """ Decodes base64 to bytes """

    return b64decode(data.encode())


def sha256(message: str) -> str:

    digest = Hash(SHA256())
    digest.update(message.encode())
    _bytes = digest.finalize()
    return b64encode(_bytes).decode()


def encrypt(message: bytes) -> bytes:
    keys = [settings.encryption_key1, settings.encryption_key2,]
    f = MultiFernet(Fernet(sha256(x)) for x in keys)
    token = f.encrypt(message)
    return token


def decrypt(token: bytes) -> bytes:
    bytes_token = token
    keys = [settings.encryption_key1, settings.encryption_key2,]
    f = MultiFernet(Fernet(sha256(x)) for x in keys)
    message = f.decrypt(bytes_token)
    return message


def encrypt_string(message: str) -> str:

    cipher_text = encrypt(message.encode())

    hex_encoded = binascii.hexlify(cipher_text).decode()

    return hex_encoded


def decrypt_string(hex_encoded: str) -> str:

    cipher_text = binascii.unhexlify(hex_encoded.encode())

    return decrypt(cipher_text).decode()


def create_jwt_token(payload: dict) -> str:
    """ Creates a JWT token """

    payload.update(
        {
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=settings.jwt_exp_hours),
            "iss":  settings.app_name,
            "iat": datetime.now(tz=timezone.utc)
        }
    )

    try:

        token = jwt.encode(payload, settings.jwt_secret,
                           algorithm=settings.jwt_algorithm)

        return token

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def decode_jwt_token(token: str) -> dict:
    """ Decodes a JWT token """

    try:

        payload = jwt.decode(token, settings.jwt_secret,
                             algorithms=[settings.jwt_algorithm])

        return payload

    except jwt.exceptions.ExpiredSignatureError as e:
        raise HTTPException(401, "unauthenticated request : expired token")

    except jwt.exceptions.InvalidIssuerError as e:
        raise HTTPException(401, "unauthenticated request : invalid issuer")

    except jwt.exceptions.DecodeError as e:
        raise HTTPException(401, "unauthenticated request : decode error")

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def hash_password(password: str) -> str:
    """ Hashes a password with scrypt """

    try:

        kdf = Scrypt(salt=settings.password_salt.encode(),
                     n=2 ** 14, r=8, p=2, length=32)

        encoded_hash = encode_base64(kdf.derive(password.encode()))

        return encoded_hash

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def verify_password(password: str, password_hash: str) -> bool:
    """ Verifies a password with scrypt """

    try:

        kdf = Scrypt(salt=settings.password_salt.encode(),
                     n=2 ** 14, r=8, p=2, length=32)

        kdf.verify(password.encode(), decode_base64(password_hash))

        return True

    except InvalidKey as e:

        return False

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def generate_otp(foreign_id, action):
    secret = os.urandom(20)
    hotp = HOTP(
        secret,
        6,
        SHA1(),
    )

    tfa = OTP(
        secret=encrypt(secret.decode()),
        foreign_id=foreign_id,
        is_active=True,
        action=action
    )
    await DB[COLS.OTPS].insert_one(tfa.model_dump())

    return hotp, tfa


async def verify_otp(uid, otp):
    pass
