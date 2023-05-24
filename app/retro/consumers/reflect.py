import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login
from retro.types import RetroSteps
from retro.models import RetroSession, CardGroup, RetroCard


class ReflectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.USER = self.scope['user']
        self.SESSION_ID = int(self.scope['url_route']['kwargs']['session_id'])
        self.GROUP_NAME = "session_%s" % self.SESSION_ID
        await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
        await self.accept()

    @sync_to_async
    def create_card(self, data):
        obj = RetroCard.objects.create(**data)
        obj.init_group(self.SESSION_ID)
        positive_cards = RetroCard.objects.filter(card_group__retro_session=self.SESSION_ID).filter(is_positive=True).count()
        negative_cards = RetroCard.objects.filter(card_group__retro_session=self.SESSION_ID).filter(is_positive=False).count()
        return json.dumps({'positive_cnt': positive_cards, 'negative_cnt': negative_cards})

    async def receive(self, text_data=None, bytes_data=None):
        json_data = json.loads(text_data)
        is_positive = bool(json_data['is_positive'])
        text = json_data['text']
        card_obj = {'text': text, 
                    'is_positive': is_positive}
        res = await self.create_card(card_obj)
        print(res)
        self.send(res)
        return res

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)