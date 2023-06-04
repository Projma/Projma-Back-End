import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from retro.types import RetroSteps
from retro.models import RetroSession, CardGroup, RetroCard


class GroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.USER = self.scope['user']
        self.SESSION_ID = int(self.scope['url_route']['kwargs']['session_id'])
        self.GROUP_NAME = "session_%s" % self.SESSION_ID
        if not await self.check_accessability():
            await self.accept()
            await self.send(json.dumps({'code': 1, 'message': 'You do not have access to this session'}))
        else:
            await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
            await self.accept()
            await self.send(json.dumps({'code': 1, 'message': 'Connected successfully'}))

    @sync_to_async
    def check_accessability(self):
        board = RetroSession.objects.get(pk=self.SESSION_ID).board
        admin = board.admins.all()
        members = board.members.all()
        wowner = board.workspace.owner
        if (not self.USER.profile in (admin | members)) and self.USER.profile != wowner:
            return False
        return True

    @sync_to_async
    def is_admin(self):
        board = RetroSession.objects.get(pk=self.SESSION_ID).board
        admin = board.admins.all()
        wowner = board.workspace.owner
        if self.USER in admin or self.USER == wowner:
            return True
        return False

    @sync_to_async
    def merge_cards(self, parent_card, card):
        card = RetroCard.objects.get(pk=card)
        card.card_group = parent_card
        card.save()

    async def show_groups(self):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        json_data = json.loads(text_data)
        if await self.is_admin():
            request_type = json_data['type']
            if request_type == "show_groups":
                p_c = json_data['parent_card']
                c = json_data['card']
                await self.merge_cards(p_c, c)
            await self.channel_layer.group_send(self.GROUP_NAME, {'type': 'show_groups'})
        else:
            self.send(json.dumps({'code': 1, 'message': 'You are not allowed.'}))