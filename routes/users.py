from fastapi import APIRouter, Depends, HTTPException, status, Query
from models.users import User, UserIn, USER_EXCLUDE_FIELDS, AccessToken
from utils.security import hash_password, create_otp, decode_base64, recover_otp
from utils.db import DB, COLS
from fastapi.security import OAuth2PasswordRequestForm
from utils.db_helpers import find_doc, update_doc
from models.enums import PKTypes
from models.enums import Actions, Emails
from utils.helper_funcs import make_email_verify_link
from tasks.actors import task_send_email
from datetime import datetime

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED, response_model_exclude=USER_EXCLUDE_FIELDS)
async def create_new_user(body:  UserIn):

    email_exists = await find_doc(COLS.USERS, "email", body.email)

    if email_exists:
        raise HTTPException(400, "email exists already")

    username_exists = await find_doc(COLS.USERS, "username", body.username)

    if username_exists:
        raise HTTPException(400, "username exists already")

    hashed_password = hash_password(body.password)

    new_user = User(
        username=body.username,
        password_hash=hashed_password,
        email=body.email
    )

    await DB[COLS.USERS].insert_one(new_user.model_dump())

    hotp, otp_doc = await create_otp(new_user.uid, Actions.VERIFY_EMAIL)

    otp = (hotp.generate(datetime.now().day)).decode()

    email_data = {
        "otp": otp,
        "username": new_user.username,
        "url": make_email_verify_link(new_user.uid, otp_doc.token)
    }

    task_send_email.send(
        new_user.email, Emails.VERIFY_EMAIL, email_data)

    return new_user


@router.get("/verify-email", status_code=status.HTTP_200_OK, response_model=dict)
async def verify_email(token_str: str = Query(alias="token")):

    uid_section, token = token_str.split(".")

    if not uid_section or not token:
        raise HTTPException(400, "Invalid token")

    user_id = decode_base64(uid_section).decode()

    print("\n", user_id, "\n")
    user = await find_doc(COLS.USERS, "uid", user_id, model=User)

    if not user:
        raise HTTPException(404, "User does not exist!")

    if user.email_verified:
        raise HTTPException(400, "Email already verified!")

    _, otp_doc = await recover_otp(token)

    if not otp_doc:
        raise HTTPException(404, "Invalid OTP")

    if otp_doc.action != Actions.VERIFY_EMAIL:
        raise HTTPException(400, "Invalid OTP")

    if not otp_doc.is_active:
        raise HTTPException(400, "OTP has expired")

    await update_doc(COLS.USERS, "uid", user_id, {
        "email_verified": True
    })

    await update_doc(COLS.OTPS, "token", token, {
        "is_active": False
    })

    return {
        "message": "Email verified successfully!"
    }


@router.post("/login", response_model=AccessToken, status_code=status.HTTP_200_OK, response_model_exclude=USER_EXCLUDE_FIELDS)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):

    user: User = await find_doc(COLS.USERS, "email", form_data.username, model=User)

    if not user:
        raise HTTPException(
            404, "We couldn't find an account with that email address.")

    if not user.check_password(form_data.password):
        raise HTTPException(401, "Invalid credentials")

    jwt_payload = {
        "sub": user.uid,
    }

    jwt_token = user.create_jwt_token(jwt_payload)

    return AccessToken(
        access_token=jwt_token,
        token_type="bearer"
    )


@router.get("/{pk}", response_model=User, status_code=status.HTTP_200_OK, response_model_exclude=USER_EXCLUDE_FIELDS)
async def get_user_by_primary_key(pk:  str, pk_type: PKTypes = Query(PKTypes.UID)):
    user = await find_doc(COLS.USERS, pk_type.value, pk, model=User)

    if not user:
        raise HTTPException(404, "user does not exist")

    return user
