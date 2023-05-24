import json
# from channels.generic.websocket import WebsocketConsumer, async_to_sync
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login
from retro.types import RetroSteps
from retro.models import RetroSession

class SessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.USER = self.scope['user']
        self.SESSION_ID = int(self.scope['url_route']['kwargs']['session_id'])
        self.GROUP_NAME = "session_%s" % self.SESSION_ID
        await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
        await self.accept()

    @sync_to_async
    def session_next(self, event):
        session = event['session']
        session.retro_step = RetroSteps.next(session.retro_step)
        session.save()
        self.send(text_data=json.dumps({'session': session.pk}))    
        return {"a": 3}

    async def get_retro_session(self):
        return RetroSession.objects.get(pk=self.SESSION_ID)

    async def receive(self, text_data):
        json_data = json.loads(text_data)
        if json_data['type'] == 'session_next':
            sync_get_data = sync_to_async(RetroSession.objects.get)
            try:
                # session = RetroSession.objects.get(pk=int(self.SESSION_ID))
                session = await sync_get_data(pk=self.SESSION_ID)
            except:
                return {
                    'code': 1,
                    'message': 'The session is invalid'
                }
            await self.channel_layer.group_send(
                self.GROUP_NAME,
                {
                    'type': 'session_next',
                    'session': session,
                    'sender_channel_name': self.channel_name
                }
            )
            

    async def disconnect(self, code):
        # self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)
        pass