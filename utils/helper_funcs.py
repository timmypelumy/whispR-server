from config.settings import get_settings
from utils.security import encode_base64
settings = get_settings()


def make_email_verify_link(user_id, token):
    url = f"{settings.frontend_url}/verify-email?token={encode_base64(user_id.encode())}.{token}"

    if settings.debug:
        print(f"Email verification link: {url}")

    return url
