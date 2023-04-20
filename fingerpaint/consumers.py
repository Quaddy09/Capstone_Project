import asyncio
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

        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        # leave the group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # remove that user from the room model
        room = await self.get_room(self.room_name)
        user = self.scope['session']['session_username']
        room_players = room.players
        room_players.remove(user)
        room.players = room_players
        await database_sync_to_async(room.save)()

        # delete that room if no one in it
        if len(room.players) == 0:
            await asyncio.sleep(10)
            await self.delete_room(room)
        # else update it
        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_player_list',
                    'players': room.players
                })

    # receive message via websocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        command = data['command']

        if command == 'join':
            # Get the list of players in the room
            room = await self.get_room(self.room_name)
            players = room.players

            # check to make sure user is not in there
            user = self.scope['session']['session_username']
            if user not in players:
                await self.add_player(user, room.room_name)
            room = await self.get_room(self.room_name)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_player_list',
                    'players': room.players
                })
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

    async def send_player_list(self, event):
        players = event['players']

        await self.send(text_data=json.dumps({
            'command': 'join',
            'players': players,
        }))

    async def send_remove(self, event):
        player_username = event['player_username']
        room = await self.get_room(self.room_name)

        # Remove the player from the room's player list
        await self.remove_player(player_username, room)

        # Send a message to the room's WebSocket group to update the players list
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_player_list',
                'players': room.players,
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # send message to websocket
        await self.send(text_data=json.dumps({
            'command': 'message',
            'message': message
        }))

    @database_sync_to_async
    def get_room(self, name):
        return Room.objects.get(room_name=name)

    @database_sync_to_async
    def add_player(self, user, name):
        room = Room.objects.get(room_name=name)
        print('in add_user = ' + user)
        print(room.players)
        if user not in room.players:
            room.players.append(user)
            print(room.players)
            room.save()
            print('added ' + user)

    @database_sync_to_async
    def remove_player(self, username, room):
        room_players = room.players
        room_players.remove(username)
        room.players = room_players
        room.save()

    @database_sync_to_async
    def delete_room(self, room):
        Room.objects.get(room_name=room).delete()

