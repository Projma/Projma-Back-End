import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login


class PollConsumemr(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # await login(self.scope, user)
        # await database_sync_to_async(self.scope["session"].save)()

    async def disconnect(self, code):
        pass
