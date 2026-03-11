import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import RoomMember

class VideoChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.uid = None

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        # Cleanup zombie record if the user disconnected abruptly
        if self.uid and self.room_name:
            await self.delete_member(self.uid, self.room_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        
        if action == 'join':
            self.uid = data['uid']
            name = data.get('name', '')
            user = self.scope.get('user')
            
            # Use authenticated user's name if available
            if user and user.is_authenticated:
                name = user.username
                
            await self.create_member(self.uid, self.room_name, name, user if user and user.is_authenticated else None)

    @database_sync_to_async
    def create_member(self, uid, room_name, name, user):
        member, created = RoomMember.objects.get_or_create(
            uid=uid,
            room_name=room_name,
            defaults={'name': name, 'user': user}
        )
        return member

    @database_sync_to_async
    def delete_member(self, uid, room_name):
        try:
            member = RoomMember.objects.get(uid=uid, room_name=room_name)
            member.delete()
        except RoomMember.DoesNotExist:
            pass
