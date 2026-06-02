from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import WebSocket

from app.websocket.ws_manager import manager
from app.services.realtime_service import RealtimeService


realtime_service = RealtimeService()


@asynccontextmanager
async def lifespan(app: FastAPI):

    import asyncio

    asyncio.create_task(
        realtime_service.run()
    )

    yield


app = FastAPI(
    title="CUSTOM Backend",
    lifespan=lifespan
)


@app.get("/health")
async def health():

    return {
        "status": "running"
    }


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):

    await manager.connect(
        websocket
    )

    try:

        while True:

            await websocket.receive_text()

    except Exception:

        manager.disconnect(
            websocket
        )