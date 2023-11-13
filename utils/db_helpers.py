from .db import COLS, DB
from config.settings import get_settings
from fastapi import HTTPException
from .pure_functions import get_utc_timestamp

settings = get_settings()


async def find_doc(col: COLS, pk, pk_value, model=None, filter:  dict = {}, raise_404=False):

    filter.update({
        pk: pk_value
    })

    doc = await DB[col].find_one(filter)

    if not doc and raise_404:
        raise HTTPException(404, f"{col.value} entry cannot be found.")

    if not doc and not raise_404:
        return None

    if model:
        return model(**doc)

    return doc


async def update_doc(col: COLS, pk, pk_value, update: dict, refresh_from_db=False, model=None):

    update.update({
        "updated_at": get_utc_timestamp()
    })

    await DB[col].update_one({pk: pk_value}, {"$set": update})

    if refresh_from_db:
        return await find_doc(col, pk, pk_value, model=model)

    return None
