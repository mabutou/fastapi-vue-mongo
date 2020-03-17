from bson.objectid import ObjectId
from fastapi import HTTPException
import logging


def validate_object_id(id: str):
    try:
        _id = ObjectId(id)
    except Exception:
        logging.warning('invalid object id')
        raise HTTPException(status_code=400, detail='invalid object id')
    return _id
