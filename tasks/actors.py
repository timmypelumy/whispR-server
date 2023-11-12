import dramatiq
import pymongo
from config.settings import get_settings
from utils.db import COLS
from utils.emails.send_mail import dispatch_email


settings = get_settings()

DB = pymongo.MongoClient(settings.db_url)[settings.db_name]


@dramatiq.actor(max_retries=3, min_backoff=30)
def say_hello_to_new_user(user_id):

    user = DB[COLS.USERS].find_one({"uid": user_id})

    if not user:
        return

    print(f"Hello {user['username']}! Welcome to whispR!")


@dramatiq.actor(max_retries=3, min_backoff=30)
def send_email(email_to, email_type, email_data):

    dispatch_email(email_to, email_type, email_data)
