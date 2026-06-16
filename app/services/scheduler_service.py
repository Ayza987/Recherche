import asyncio

from app.config import COLLECTION_INTERVAL

from app.api.websocket import manager

from app.database.database import SessionLocal

from app.database.repository import (
    SensorRepository
)

from app.services.collector_service import (
    CollectorService
)


collector = CollectorService()


async def collector_loop():

    while True:

        try:

            sensors = collector.collect()

            db = SessionLocal()

            for sensor in sensors:

                SensorRepository.save(
                    db,
                    sensor
                )

            await manager.broadcast(
                sensors
            )

            db.close()

            await asyncio.sleep(
                COLLECTION_INTERVAL
            )

        except Exception as e:

            print(e)

            await asyncio.sleep(5)