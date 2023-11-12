from fastapi import APIRouter, Depends, HTTPException, status, Query
from models.users import User, UserIn, USER_EXCLUDE_FIELDS, AccessToken
from utils.security import hash_password
from utils.db import DB, COLS
from fastapi.security import OAuth2PasswordRequestForm
from utils.db_helpers import find_doc
from models.enums import PKTypes

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

    return new_user


@router.get("/{pk}", response_model=User, status_code=status.HTTP_200_OK, response_model_exclude=USER_EXCLUDE_FIELDS)
async def get_user_by_primary_key(pk:  str, pk_type: PKTypes = Query(PKTypes.UID)):
    user = await find_doc(COLS.USERS, pk_type.value, pk, model=User)

    if not user:
        raise HTTPException(404, "user does not exist")

    return user


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
