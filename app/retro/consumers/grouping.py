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
        retro = RetroSession.objects.get(pk=self.SESSION_ID)
        if self.USER.profile == retro.admin:
            return True
        return False

    @sync_to_async
    def merge_cards(self, parent_card, card):
        card = RetroCard.objects.get(pk=card)
        card.card_group = parent_card
        card.save()

    @sync_to_async
    def split_cards(self, card_id, card_text):
        pre_group = CardGroup.objects.filter(name=card_text).first()
        card = RetroCard.objects.get(pk=card_id)
        card.card_group = pre_group
        card.save()

    async def show_groups(self):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        json_data = json.loads(text_data)
        if await self.is_admin():
            request_type = json_data['type']
            if request_type == "merge":
                p_c = json_data['data']['parent_card']
                c = json_data['data']['card']
                await self.merge_cards(p_c, c)
            elif request_type == 'split':
                c_id = json_data['data']['id']
                c_text = json_data['data']['text']
                await self.split_cards(c_id, c_text)
            await self.channel_layer.group_send(self.GROUP_NAME, {'type': 'show_groups'})
        else:
            self.send(json.dumps({'code': 1, 'message': 'You are not allowed.'}))