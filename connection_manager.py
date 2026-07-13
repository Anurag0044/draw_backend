from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # Store all active WebSocket connections
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # Accept the WebSocket connection
        await websocket.accept()

        # Add the client to the active connections list
        self.active_connections.append(websocket)

        print(f"Client connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        # Remove the client if it exists
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

        print(f"Client disconnected. Total clients: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        # Send a message to one specific client
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        # Send the same message to every connected client
        for connection in self.active_connections:
            await connection.send_text(message)