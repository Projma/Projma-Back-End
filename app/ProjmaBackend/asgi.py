"""
ASGI config for ProjmaBackend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

import retro.routing
from ProjmaBackend.channelsmiddleware import JwtAuthMiddlewareStack
from django.core.asgi import get_asgi_application

import board.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjmaBackend.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
            JwtAuthMiddlewareStack(
                URLRouter(
                    # board.routing.websocket_urlpatterns,
                    retro.routing.websocket_urlpatterns,
                )
            ),
        ),
}) 
