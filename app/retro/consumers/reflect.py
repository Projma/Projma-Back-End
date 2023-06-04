import json
from asgiref.sync import sync_to_async
from retro.consumers.session import SessionConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login
from retro.types import RetroSteps
from retro.models import RetroSession, CardGroup, RetroCard


class ReflectConsumer(SessionConsumer):
    async def connect(self, *args, **kwargs):
        return await super().connect(step_name='reflect')

    @sync_to_async
    def create_card(self, data):
        obj = RetroCard.objects.create(**data)
        obj.init_group(self.SESSION_ID)

    @sync_to_async
    def get_query(self):
        positive_cards = RetroCard.objects.filter(card_group__retro_session=self.SESSION_ID).filter(is_positive=True).count()
        negative_cards = RetroCard.objects.filter(card_group__retro_session=self.SESSION_ID).filter(is_positive=False).count()
        return {'positive_cnt': positive_cards, 'negative_cnt': negative_cards}

    async def receive(self, text_data=None, bytes_data=None):
        typ, data = await super().receive(text_data, bytes_data)
        if typ == 'create_card':
            is_positive = bool(data['is_positive'])
            text = data['text']
            card_obj = {'text': text,
                        'is_positive': is_positive}
            await self.create_card(card_obj)
            await self.channel_layer.group_send(self.GROUP_NAME,{
                'type': 'send_nums',
                'data': await self.get_query()
            })
        
    async def send_nums(self, event):
        await self.send(text_data=json.dumps(event))
