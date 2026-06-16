import asyncio

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

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

    print("Collecte temps réel démarrée")

    yield

    task.cancel()

    print("Collecte arrêtée")


app = FastAPI(
    title="CUSTOM API",
    lifespan=lifespan
)


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


BASE_DIR = Path(__file__).resolve().parent.parent

app.mount(
    "/",
    StaticFiles(
        directory=BASE_DIR / "frontend",
        html=True
    ),
    name="frontend"
)