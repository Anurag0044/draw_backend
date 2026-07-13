from fastapi import WebSocket, WebSocketDisconnect

# Store all connected clients
connected_clients = []


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    connected_clients.append(websocket)

    print("Client Connected")

    try:
        while True:
            message = await websocket.receive_text()

            print("Received:", message)

            # Send the message back to the same client
            await websocket.send_text(f"Server received: {message}")

    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print("Client Disconnected")