from fastapi import Depends, FastAPI, Header, HTTPException
from database.mongodb import connect_to_mongo, close_mongo_connectin
import asyncio
from database.mongodb import db
from vps.routes import vps_router

app = FastAPI(title="mc's VPS API",
              description="About VPS Info",
              version="0.0.1")
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connectin)

app.include_router(vps_router,
                   prefix='/vps',
                   tags=['vps'],
                   responses={404: {
                       'description': 'path error!'
                   }})
