import asyncio

from app.config import COLLECTION_INTERVAL

from app.api.websocket import manager

from app.database.database import SessionLocal

from app.database.repository import (
    SensorRepository
)
from app.services.master_service import (
    MasterService
)


master = MasterService()


async def collector_loop():

    while True:

        try:

            data = master.collect()

            db = SessionLocal()

            for sensor in data["ports"]:

                SensorRepository.save(
                    db,
                    sensor
                )

            await manager.broadcast(
                data
            )

            db.close()

            await asyncio.sleep(
                COLLECTION_INTERVAL
            )

        except Exception as e:

            print(e)

            await asyncio.sleep(5)