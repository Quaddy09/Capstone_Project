from django.urls import path
from .consumers import GameConsumer

websocket_urlpatterns = [
    path('ws/home/<str:room_name>', GameConsumer.as_asgi())
]