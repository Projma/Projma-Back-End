from django.urls import re_path
from retro.consumers.vote import VoteConsumer
from retro.consumers.session import SessionConsumer
from retro.consumers.reflect import ReflectConsumer
from retro.consumers.grouping import GroupConsumer

websocket_urlpatterns = {
    re_path(r'ws/socket-server/vote/(?P<session_id>\w+)/', VoteConsumer.as_asgi()),
    re_path(r'ws/socket-server/retro/session/(?P<session_id>\w+)/', SessionConsumer.as_asgi()),
    re_path(r'ws/socket-server/retro/reflect/(?P<session_id>\w+)/', ReflectConsumer.as_asgi()),
    re_path(r'ws/socket-server/retro/grouping/(?P<session_id>\w+)/', GroupConsumer.as_asgi()),
}
