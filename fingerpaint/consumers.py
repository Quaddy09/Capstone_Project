import json

from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from .models import Lobby
from classes import myUser


class GameConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        # Get the roomName variable from the event or from your view
        room_name = self.scope['url_route']['kwargs']['room_name']

        player = Lobby(roomName=room_name, players=self.scope['session']['session_username'])
        player.save()

        game_room = Lobby.objects.get(room_name=self.room_name)
        usernames = [game_room.players for player in game_room]

        # Send the roomName variable to the client after the WebSocket connection is established
        await self.send(text_data=json.dumps({'usernames': usernames}))

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'game_%s' % self.room_name

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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # Handle received message, update game state, etc.
        # Send updated game state to all players in the room


        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_message',
                'message': text_data_json
            }
        )

    async def game_message(self, event):
        message = event['message']

        await self.send(json.dumps({
            'type': 'game_state',
            'message': message
        }))


'''
class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()


class DrawerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.lobby_name = self.scope['url_route']['kwargs']['lobby_name']
        self.lobby_group_name = f'drawing_{self.lobby_name}'

        # Join lobby group
        await self.channel_layer.group_add(
            self.lobby_group_name,
            self.channel_name
        )

        # Send prompt to drawer
        prompt = 'This is your prompt!'
        await self.send(text_data=json.dumps({
            'prompt': prompt
        }))

    async def disconnect(self, close_code):
        # Leave lobby group
        await self.channel_layer.group_discard(
            self.lobby_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Broadcast drawing data to all clients in lobby
        await self.channel_layer.group_send(
            self.lobby_group_name,
            {
                'type': 'drawing_data',
                'data': json.loads(text_data)
            }
        )

    async def drawing_data(self, event):
        # Send drawing data to all clients in lobby
        await self.send(text_data=json.dumps(event['data']))


class GuesserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.lobby_name = self.scope['url_route']['kwargs']['lobby_name']
        self.lobby_group_name = f'drawing_{self.lobby_name}'

        # Join lobby group
        await self.channel_layer.group_add(
            self.lobby_group_name,
            self.channel_name
        )

        # Send current drawing to guesser
        current_drawing = None  # get current drawing from database or other storage mechanism
        if current_drawing:
            await self.send(text_data=json.dumps({
                'drawing_data': current_drawing
            }))

    async def disconnect(self, close_code):
        # Leave lobby group
        await self.channel_layer.group_discard(
            self.lobby_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Process guess from user
        guess = json.loads(text_data)['guess']
        # Save guess to database or other storage mechanism

    async def drawing_data(self, event):
        # Send updated drawing to guesser
        await self.send(text_data=json.dumps({
            'drawing_data': event['data']
        }))
'''

