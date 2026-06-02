import asyncio

from app.services.collector_service import CollectorService
from app.websocket.ws_manager import manager


class RealtimeService:

    def __init__(self):

        self.collector = CollectorService()


    async def run(self):

        while True:

            data = await self.collector.collect()

            await manager.broadcast(data)

            await asyncio.sleep(2)