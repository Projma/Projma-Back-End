from django.urls import re_path
from retro.consumers.vote import VoteConsumer

websocket_urlpatterns = {
    re_path(r'ws/socket-server/vote', VoteConsumer.as_asgi()),
}
