from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidKey
from config.settings import get_settings
from base64 import b64encode, b64decode
from fastapi import HTTPException, status


settings = get_settings()


def encode_base64(data: bytes) -> str:
    
        """ Encodes bytes to base64 """
    
        return b64encode(data).decode()

def decode_base64(data: str) -> bytes:
    
        """ Decodes base64 to bytes """
    
        return b64decode(data.encode())


def hash_password(password: str) -> str:

    """ Hashes a password with scrypt """

    try:

        kdf = Scrypt(salt= settings.password_salt.encode(),  n=2 ** 14, r=8, p=2, length=32)

        encoded_hash =  encode_base64(kdf.derive(password.encode()))

        return encoded_hash
    
    except Exception as e:
              
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def verify_password(password: str, password_hash: str) -> bool:

    """ Verifies a password with scrypt """

    try:

        kdf = Scrypt(salt= settings.password_salt.encode(), n=2 ** 14, r=8, p=2, length=32)

        kdf.verify(password.encode(), decode_base64(password_hash))

        return True
    
    except InvalidKey as e:
            
            return False
    
    except Exception as e:
        
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))