from config.settings import get_settings
from utils.security import encode_base64
settings = get_settings()


def make_email_verify_link(email, token):
    return f"{settings.frontend_url}/verify-email/{encode_base64(email.encode())}---{token}"
