import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room
from asgiref.sync import sync_to_async


class GameConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None


    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = self.room_name
        # await self.create_room()

        # get username from session
        self.user = self.scope['session']['session_username']
        try:
            self.room = await sync_to_async(Room.objects.get)(room_name=self.room_name)
        except Room.DoesNotExist:
            self.room = await database_sync_to_async(Room.objects.create)(room_name=self.room_name)

        # add players in room to Room players field
        await self.add_player()

        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        # leave the group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # delete that room if no one in it
        print(len(self.room.players))
        if len(self.room.players) == 0:
            await self.delete_room()

        # remove that user from the room model
        self.room = await sync_to_async(Room.objects.get)(room_name=self.room_name)
        await self.remove_player()

    # receive message via websocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        command = data['command']
        # message = text_data_json["message"]

        if command == 'get_players':
            # Get the list of players in the room
            self.room = await sync_to_async(Room.objects.get)(room_name=self.room_name)
            players = self.room.players
            # senf the list of players to client
            await self.send(text_data=json.dumps({
                'command': 'players_list',
                'players': players
            }))
        elif command == 'new_message':
            # get message data
            message = data['message']
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message
                }
            )
        else:
            print('unknown command received')

    async def chat_message(self, event):
        message = event['message']

        # send message to websocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def add_player(self):
        self.room.players.append(self.user)
        self.room.save()

    @database_sync_to_async
    def remove_player(self):
        self.room.players.remove(self.user)
        self.room.save()

    @database_sync_to_async
    def delete_room(self):
        self.room.delete()
