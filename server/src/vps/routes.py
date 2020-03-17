from fastapi import APIRouter, Depends, HTTPException
from typing import List
from starlette.status import HTTP_201_CREATED
from database.mongodb import db
from .model import vpsKind, vpsBase, vpsBaseUpdateRequest
from database.mongodb_validators import validate_object_id
import pprint
vps_router = APIRouter()


# add vps's _id value
def fix_vps_id(vps):
    if vps.get("_id", False):
        # change ObjectID to string
        vps["_id"] = str(vps["_id"])
        return vps
    else:
        raise ValueError(
            f"No `_id` found! Unable to fix vps ID for vps: {vps}")


# get vps date.
async def get_vps_or_404(id: str):
    _id = validate_object_id(id)
    vps = await db.mcDB.find_one({'_id': _id})
    if vps:
        return fix_vps_id(vps)
    else:
        raise HTTPException(status_code=404, detail='name error!')


@vps_router.post('/addVps', status_code=HTTP_201_CREATED)
async def add_vps(vps: vpsBase):
    vpss = vps.dict()
    vps_in = await db.mcDB.insert_one(vpss)
    if vps_in.inserted_id:
        vps = await get_vps_or_404(vps_in.inserted_id)
        return vps