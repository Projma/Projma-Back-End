from django.urls import re_path
from retro.consumers.vote import VoteConsumer
from retro.consumers.session import SessionConsumer
from retro.consumers.reflect import ReflectConsumer
from retro.consumers.group import GroupConsumer
from retro.consumers.discuss import DiscussConsumer

websocket_urlpatterns = {
    re_path(r'ws/socket-server/retro/vote/(?P<session_id>\w+)/', VoteConsumer.as_asgi()),
    re_path(r'ws/socket-server/retro/session/(?P<session_id>\w+)/', SessionConsumer.as_asgi()),
    re_path(r'ws/socket-server/retro/reflect/(?P<session_id>\w+)/', ReflectConsumer.as_asgi()),
    re_path(r'ws/socket-server/retro/group/(?P<session_id>\w+)/', GroupConsumer.as_asgi()),
    re_path(r'ws/socket-server/retro/discuss/(?P<session_id>\w+)/', DiscussConsumer.as_asgi()),
}
