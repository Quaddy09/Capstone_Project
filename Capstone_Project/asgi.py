"""
ASGI config for Capstone_Project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
from fingerpaint.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    # Use the URLRouter to route WebSocket requests
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
    # Use the default Django ASGI application for other protocols
    'http': get_asgi_application(),
    # add more protocols and corresponding applications here as needed
})
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Capstone_Project.settings')

#application = ProtocolTypeRouter({
#    'http': get_asgi_application(),
#    'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns))
#})
#    #get_asgi_application()


