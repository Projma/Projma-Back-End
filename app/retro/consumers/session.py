import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login
from retro.types import RetroSteps
from retro.models import RetroSession, CardGroup, RetroCard


class SessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.USER = self.scope['user']
        self.SESSION_ID = int(self.scope['url_route']['kwargs']['session_id'])
        self.GROUP_NAME = "session_%s" % self.SESSION_ID
        await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        json_data = json.loads(text_data)
        data = json_data['data']
        typ = json_data['type']
        if typ == 'next_step':
            sess = await sync_to_async(RetroSession.objects.get)(id=self.SESSION_ID)
            sess.retro_step += 1
            await sync_to_async(sess.save)()
            await self.channel_layer.group_send(self.GROUP_NAME,{
                'type': typ,
                'data': data,
                'sender_channel_name': self.channel_name,
            })
        return typ, data

    async def next_step(self, event):
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps(event))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)