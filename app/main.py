import asyncio

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from app.api.websocket import manager

from app.database.database import (
    Base,
    engine
)

from app.services.scheduler_service import (
    collector_loop
)


Base.metadata.create_all(
    bind=engine
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    task = asyncio.create_task(
        collector_loop()
    )

    yield

    task.cancel()


app = FastAPI(
    title="CUSTOM API",
    lifespan=lifespan
)


@app.get("/")
async def root():

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

    except WebSocketDisconnect:

        manager.disconnect(
            websocket
        )