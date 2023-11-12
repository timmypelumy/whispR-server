import smtplib
from pydantic import EmailStr
from config.settings import get_settings
from config.email_config import EMAIL_DEFS
from email.message import EmailMessage
from email.headerregistry import Address
from jinja2 import Environment, PackageLoader, select_autoescape
from config.settings import get_settings


settings = get_settings()


env = Environment(
    loader=PackageLoader("utils.emails", "templates"),
    autoescape=select_autoescape()
)


def render_to_string(template_name: str, **kwargs):
    template = env.get_template(template_name)
    return template.render(**kwargs, settings=settings)


def dispatch_email(email_to: list[EmailStr] | EmailStr, email_type: str, email_data: dict):

    if not email_type in EMAIL_DEFS:
        raise ValueError("Invalid email type")

    conf = EMAIL_DEFS[email_type]

    try:

        with smtplib.SMTP(settings.mail_server, settings.mail_port) as smtp:
            smtp.starttls()
            smtp.login(settings.mail_username, settings.mail_password)
            email_content = render_to_string(
                conf['template_name'], **email_data)

            msg = EmailMessage()
            msg['Subject'] = conf['subject']
            msg['From'] = Address(
                settings.mail_display_name, settings.mail_domain_username, settings.mail_domain)
            msg['To'] = email_to if isinstance(
                email_to, str) else ",".join(email_to)

            msg.set_content(email_content, subtype="html")

            smtp.sendmail(conf['mail_from'], email_to, msg.as_string())

    except Exception as e:

        raise Exception("Email failed to send")
