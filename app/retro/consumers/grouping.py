import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from retro.types import RetroSteps
from retro.models import RetroSession, CardGroup, RetroCard
from .session import SessionConsumer


class GroupConsumer(SessionConsumer):
    async def connect(self):
        return await super().connect(step_name='grouping')

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