import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login
from retro.types import RetroSteps
from retro.models import RetroSession, CardGroup, RetroCard


class SessionConsumer(AsyncWebsocketConsumer):
    async def connect(self, *args, **kwargs):
        self.USER = self.scope['user']
        self.SESSION_ID = int(self.scope['url_route']['kwargs']['session_id'])
        step_name = kwargs.get('step_name')
        if not step_name:
            step_name = 'start'
        self.GROUP_NAME = f'session_{self.SESSION_ID}_{step_name}'
        if not await self.check_accessability():
            await self.accept()
            await self.send(json.dumps({'code': 1, 'message': 'You do not have access to this session'}))
        else:
            await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
            await self.accept()
            await self.send(json.dumps({'code': 0, 'message': 'Connected successfully'}))

    @sync_to_async
    def check_accessability(self):
        board = RetroSession.objects.get(pk=self.SESSION_ID).board
        admin = board.admins.all()
        members = board.members.all()
        wowner = board.workspace.owner
        if (not self.USER.profile in (admin | members)) and self.USER.profile != wowner:
            return False
        return True

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