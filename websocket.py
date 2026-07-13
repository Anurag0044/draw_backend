from fastapi import WebSocket, WebSocketDisconnect
from connection_manager import ConnectionManager
from game_manager import GameManager

# Create one manager object
manager = ConnectionManager()
game_manager = GameManager()

async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    room_id = game_manager.find_available_room()
    game_manager.join_room(room_id, websocket)

    print(f"Player joined {room_id}")

    try:
        while True:
            # Receive a message from the client
            message = await websocket.receive_text()

            print(f"Received: {message}")

            # Send the message back to the same client
            await game_manager.broadcast_to_room(
                room_id,
                message
            )

    except WebSocketDisconnect:
        # Remove the client when it disconnects
        manager.disconnect(websocket)
        game_manager.leave_room(room_id, websocket)

        print(f"Player left {room_id}")