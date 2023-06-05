import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from retro.types import RetroSteps
from retro.models import RetroSession, CardGroup, RetroCard
from .session import SessionConsumer
from retro.serializers.groupserializer import GroupsWithCardsSerializer


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
        parent_card = RetroCard.objects.get(pk=parent_card).card_group
        pre_parent = card.card_group
        pre_parent.delete()
        card.card_group = parent_card
        card.save()

    @sync_to_async
    def split_cards(self, card_id):
        card = RetroCard.objects.get(pk=card_id)
        # if card.text != card.card_group.name:
        card.init_group(self.SESSION_ID)
        card.save()

    @sync_to_async
    def get_groups(self):
        groups = CardGroup.objects.filter(retro_session=self.SESSION_ID).all()
        serializer = GroupsWithCardsSerializer(groups, many=True)
        return serializer.data

    async def show_groups(self, *args, **kwargs):
        qs = await self.get_groups()
        await self.send(json.dumps(qs))

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
                await self.split_cards(c_id)
            await self.channel_layer.group_send(self.GROUP_NAME, {'type': 'show_groups'})
        else:
            self.send(json.dumps({'code': 1, 'message': 'You are not allowed.'}))