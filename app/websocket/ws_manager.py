# Gestionnaire WebSocket
from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):

        self.connections = []


    async def connect(
        self,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.connections.append(websocket)


    def disconnect(
        self,
        websocket: WebSocket
    ):

        self.connections.remove(websocket)


    async def broadcast(
        self,
        data
    ):

        disconnected = []

        for connection in self.connections:

            try:

                await connection.send_json(data)

            except Exception:

                disconnected.append(connection)

        for connection in disconnected:

            self.disconnect(connection)


manager = ConnectionManager()