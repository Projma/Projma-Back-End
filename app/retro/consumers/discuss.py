import json
from asgiref.sync import sync_to_async
from retro.consumers.session import SessionConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login
from retro.types import RetroSteps
from retro.models import RetroSession, CardGroup, RetroCard


class DiscussConsumer(SessionConsumer):
    async def connect(self, *args, **kwargs):
        return await super().connect(step_name='discuss')

    async def receive(self, text_data=None, bytes_data=None):
        typ, data = await super().receive(text_data, bytes_data)
