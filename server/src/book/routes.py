from fastapi import APIRouter, Depends, HTTPException
from typing import List
from starlette.status import HTTP_201_CREATED
from database.mongodb import db
from vps.model import vpsKind, vpsBase, vpsBaseUpdateRequest
from book.model import Book, PongResponse, BOOKS, ResponseBase, BookResponse, ListBooksResponse
from database.mongodb_validators import validate_object_id
import pprint
from starlette.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
book_router = APIRouter()


# add vps's _id value
def fix_id(vps):
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
        return fix_id(vps)
    else:
        raise HTTPException(status_code=404, detail='name error!')


#: Mount routes
@book_router.get("/api")
def index():
    return {
        "status": "ok",
        "code": 200,
        "data": "Welcome, please check /docs or /redoc",
    }


@book_router.get("/api/ping", response_model=PongResponse)
def return_pong():
    return {"status": "ok", "code": 200}


@book_router.get("/api/books", response_model=ListBooksResponse)
async def get_all_books():
    all_books = db.mcDB.find()
    BOOKS = await all_books.to_list(length=3)
    return {"status": "ok", "code": 200, "data": BOOKS}


@book_router.get("/api/books/{hostname}", response_model=BookResponse)
async def get_books(hostname: str):
    book = await db.mcDB.find_one({'hostname': hostname})
    # 通过ObjectId()，获取详细信息
    book = await get_vps_or_404(book.get('_id'))
    return {"status": "ok", "code": 200, "data": book}


@book_router.post("/api/books", status_code=201)
async def create_book(book: Book):
    book = book.dict()
    book_in = await db.mcDB.insert_one(book)
    if book_in.inserted_id:
        book = await get_vps_or_404(book_in.inserted_id)
        return {
            "status": "success",
            "code": 201,
            "messages": ["Book added !"],
            "data": book
        }


@book_router.put("/api/books/{hostname}")
async def edit_book(hostname: str, book: Book):
    book = book.dict()
    # 去除字典null值
    book = {k: v for k, v in book.items() if v}
    # return book
    vps_op = await db.mcDB.update_one({"hostname": hostname}, {"$set": book})
    if vps_op.modified_count:
        # pprint.pprint(vps_op.dict())
        book = await db.mcDB.find_one({'hostname': hostname})
        book = await get_vps_or_404(book.get('_id'))
        return {
            "status": "success",
            "code": 200,
            "messages": ["Book edited !"],
            "data": book,
        }


@book_router.delete("/api/books/{hostname}")
async def remove_book(hostname: str):
    book_op = await db.mcDB.delete_one({"hostname": hostname})
    if book_op.deleted_count:
        return {
            "status": "success",
            "code": 200,
            "messages": ["Book removed !"],
            "data": hostname,
        }