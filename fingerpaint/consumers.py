import json

from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from .models import Lobby


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
