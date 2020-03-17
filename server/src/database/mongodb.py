import logging
from motor.motor_asyncio import AsyncIOMotorClient


class DataBase:
    client: AsyncIOMotorClient = None
    mcDB = None


db = DataBase()


async def connect_to_mongo():
    logging.info("connecting to mongo...")
    db.client = AsyncIOMotorClient(
        str("mongodb://root:example@127.0.0.1:27017/"),
        maxPoolSize=10,
        minPoolsize=10)
    db.mcDB = db.client.mc.vps
    # result = await db.mcDB.insert_many([{'i': i} for i in range(200)])
    logging.info("connected to mc/vps!")


async def close_mongo_connectin():
    logging.info("closing connection...")
    db.client.close()
    logging.info("closed conection!")
