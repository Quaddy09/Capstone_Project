from django.urls import path
from .consumers import WSConsumer

ws_urlpatterns = [
    path('ws/some_path', WSConsumer.as_asgi())
]