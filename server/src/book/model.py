from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime, date


#: Initialize list of books
class Book(BaseModel):
    title: str = None
    author: str = None
    read: bool = None
    hostname: str = None
    ip: str = None
    port: int = None
    username: str = None
    password: str = None
    cpu: str = None
    memory: str = None
    online: bool = None


BOOKS: List[Book] = []


#: Describe all Pydantic Response classes
class ResponseBase(BaseModel):
    status: str
    code: int
    messages: List[str] = []


class PongResponse(ResponseBase):
    data: str = "Pong!"


class BookResponse(ResponseBase):
    data: Book


class ListBooksResponse(ResponseBase):
    data: List[Book]
