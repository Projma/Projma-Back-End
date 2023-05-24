from django.urls import re_path
from retro.consumers.vote import VoteConsumer
from retro.consumers.session import SessionConsumer
from retro.consumers.reflect import ReflectConsumer

websocket_urlpatterns = {
    re_path(r'ws/socket-server/vote', VoteConsumer.as_asgi()),
    re_path(r'ws/socket-server/retro/session/(?P<session_id>\w+)/', SessionConsumer.as_asgi()),
    re_path(r'ws/socket-server/retro/reflect/(?P<session_id>\w+)/', ReflectConsumer.as_asgi()),
}
