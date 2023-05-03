from django.urls import re_path
from board.consumers.poll import PollConsumemr

websocket_urlpatterns = {
    re_path(r'ws/socket-server/', PollConsumemr.as_asgi())
}
