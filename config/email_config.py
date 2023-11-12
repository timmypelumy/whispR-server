from config.settings import get_settings
from models.enums import Emails

settings = get_settings()

EMAIL_DEFS = {
    Emails.VERIFY_EMAIL: {
        'subject': "Verify Your Email",
        'mail_from': settings.mail_from,
        'template_name': "verify_email.html",
    },


}
