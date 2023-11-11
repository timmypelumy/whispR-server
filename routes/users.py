from fastapi import APIRouter, Depends, HTTPException, status
from models.users import User, UserIn
from utils.security import hash_password
from utils.db import DB, COLS
from utils.db_helpers import find_doc


router = APIRouter(prefix="/users")

@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_new_user( body :  UserIn):

    email_exists =  await find_doc(COLS.USERS, "email", body.email)

    if email_exists:
        raise HTTPException(400, "email exists already")

    username_exists  = await find_doc(COLS.USERS, "username", body.username)

    if username_exists:
        raise HTTPException(400, "username exists already")
    
    hashed_password  = hash_password(body.password)

    new_user =  User(
        username=body.username,
        password_hash= hashed_password,
        email=body.email
    )

    await DB[COLS.USERS].insert_one(new_user.model_dump())


    return new_user
    

    
