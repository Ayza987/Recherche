import asyncio

from app.services.collector_service import CollectorService

from app.websocket.ws_manager import manager

from app.database.repository import ReadingRepository


class RealtimeService:

    def __init__(self):

        self.collector = CollectorService()

        self.repository = ReadingRepository()


    async def run(self):

        while True:

            data = await self.collector.collect()

            self.repository.save_reading(
                sensor_id=1,
                operating_hours=data["operating_hours"],
                power_cycles=data["power_cycles"],
                device_status=data["device_status"]
            )

            await manager.broadcast(data)

            await asyncio.sleep(2)