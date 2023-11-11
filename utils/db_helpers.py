from .db import COLS,DB
from config.settings import get_settings
from fastapi import HTTPException

settings = get_settings()

async def find_doc( col : COLS,pk, pk_value, model = None, filter :  dict = {}, raise_404 = False ):

    filter.update({
        pk : pk_value
    })

    doc = await DB[col].find_one(filter)

    if not doc and raise_404:
        raise HTTPException(404, f"{col.value} entry cannot be found.")
    
    if not doc and not raise_404:
        return None
    
    if model:
        return model(**doc)
    
    return doc


