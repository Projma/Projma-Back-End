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
        if parent_card != card:
            card = RetroCard.objects.get(pk=card)
            parent_card = RetroCard.objects.get(pk=parent_card).card_group
            pre_parent = card.card_group
            if pre_parent != parent_card:
                card.card_group = parent_card
                card.save()
                if not len(pre_parent.retro_cards.all()):
                    pre_parent.delete()

    @sync_to_async
    def split_cards(self, card_id):
        card = RetroCard.objects.get(pk=card_id)
        if card.text != card.card_group.name:
            parent_card = card.card_group
            card.init_group(self.SESSION_ID)
            card.save()
            if not (parent_card.retro_cards.all()):
                parent_card.delete()

    @sync_to_async
    def get_groups(self):
        groups = CardGroup.objects.filter(retro_session=self.SESSION_ID).all()
        serializer = GroupsWithCardsSerializer(groups, many=True)
        return serializer.data

    async def show_groups(self, *args, **kwargs):
        qs = await self.get_groups()
        await self.send(json.dumps(qs))

    async def receive(self, text_data=None, bytes_data=None):
        typ, data = await super().receive(text_data, bytes_data)

        if await self.is_admin():
            if typ == "merge":
                p_c = data['parent_card']
                c = data['card']
                await self.merge_cards(p_c, c)
                await self.channel_layer.group_send(self.GROUP_NAME, {'type': 'show_groups'})
            elif typ == 'split':
                c_id = data['id']
                await self.split_cards(c_id)
                await self.channel_layer.group_send(self.GROUP_NAME, {'type': 'show_groups'})
        else:
            await self.send(json.dumps({'code': 1, 'message': 'You are not allowed.'}))