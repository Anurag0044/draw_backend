class GameManager:
    def __init__(self):
        # Stores all game rooms
        self.rooms = {}

    def create_room(self, room_id: str):
        """Create a new room."""
        if room_id not in self.rooms:
            self.rooms[room_id] = {
                "players": [],
                "game_started": False,
                "prompt": None,
                "scores": {}
            }

    def join_room(self, room_id: str, websocket):
        """Add a player to a room."""
        if room_id not in self.rooms:
            self.create_room(room_id)

        self.rooms[room_id]["players"].append(websocket)

    def leave_room(self, room_id: str, websocket):
        """Remove a player from a room."""
        if room_id in self.rooms:
            if websocket in self.rooms[room_id]["players"]:
                self.rooms[room_id]["players"].remove(websocket)

            # Delete empty room
            if len(self.rooms[room_id]["players"]) == 0:
                del self.rooms[room_id]

    def get_players(self, room_id: str):
        """Return all players in a room."""
        if room_id in self.rooms:
            return self.rooms[room_id]["players"]

        return []
        
    async def broadcast_to_room(self, room_id: str, message: str):
        """
        Send a message to every player in the room.
        """

        if room_id not in self.rooms:
            return

        for player in self.rooms[room_id]["players"]:
            await player.send_text(message)
    
    def find_available_room(self):
        """
        Find a room with fewer than 2 players.
        If no room is available, create a new one.
        """

        # Check existing rooms
        for room_id, room in self.rooms.items():
            if len(room["players"]) < 2:
                return room_id

        # No available room, create a new one
        room_number = len(self.rooms) + 1
        new_room = f"room{room_number}"

        self.create_room(new_room)

        return new_room
   