from channels.generic.websocket import AsyncWebsocketConsumer
from .services import get_private_chat_room
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    """Handle WebSocket connections for private chat."""

    async def connect(self):
        print("1. Connect called")
        user = self.scope["user"]
        print("2. User:", user)

        room_id = self.scope["url_route"]["kwargs"]["room_id"]
        print("3. Room ID:", room_id)

        room = await sync_to_async(get_private_chat_room)(
            room_id,
            user
        )
        print("4. Room:", room.id)

        if room is None:
            print("5. Room not found")
            await self.close()
            return
        
        self.room = room
        self.room_id = str(room.id)
        self.room_group_name = f"chat_{self.room_id}"
        print("6. Before group_add")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        print("7. After group_add")
        await self.accept()

        print("8. Accepted")


    async def disconnect(self, close_code):
        print("DISCONNECTED", close_code)

    async def disconnect(self, close_code):
        print("Disconnected:", close_code)
        """Handle WebSocket disconnection."""
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        pass