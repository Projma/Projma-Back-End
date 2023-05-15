from django.urls import re_path
from board.consumers.poll import PollConsumemr
from board.consumers.board import BoardConsumer

websocket_urlpatterns = {
    re_path(r'ws/socket-server/', PollConsumemr.as_asgi()),
    re_path(r'ws/socket-server/board', BoardConsumer.as_asgi())
}
