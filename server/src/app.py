from typing import List
from fastapi import Depends, FastAPI, Header, HTTPException
from database.mongodb import connect_to_mongo, close_mongo_connectin
import asyncio
from database.mongodb import db
from vps.routes import vps_router
from book.routes import book_router
from pydantic import BaseModel
from book.model import Book, BOOKS
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response, UJSONResponse

# from book.routes import startup_event
app = FastAPI(title="mc's VPS API",
              description="About VPS Info",
              version="0.0.1")
#: Configure COR
origins = [
    "http://localhost:8080",
    "http://huawei:8080",
    "http://huawei:5500",
    "http://121.37.9.206:8080",
    "http://192.168.10.23:9528",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connectin)

app.include_router(vps_router,
                   prefix='/vps',
                   tags=['vps'],
                   responses={404: {
                       'description': 'path error!'
                   }})
app.include_router(book_router,
                   prefix='',
                   tags=['book'],
                   responses={404: {
                       'description': 'path error!'
                   }})


@app.on_event("startup")
async def startup_event():
    BOOKS.clear()
    BOOKS.append(Book(title="On the Road", author="Jack Kerouac", read=True))
    BOOKS.append(
        Book(
            title="Harry Potter and the Philosopher's Stone",
            author="J. K. Rowling",
            read=False,
        ))
    BOOKS.append(
        Book(title="Green Eggs and Ham", author="Dr. Seuss", read=True))


#: Start application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)