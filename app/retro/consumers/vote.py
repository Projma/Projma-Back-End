import json
from channels.generic.websocket import WebsocketConsumer, async_to_sync
from channels.auth import login
from retro.models import RetroSession


class VoteConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        board = self.scope['board']

        self.room_group_name = str(board.id)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': f'{user.username} has opened to the board'
        #     }
        # )
        # self.send(json.dumps({
        #     'type': 'Test Message For Channel Connectivity',
        #     'message': 'madar chini',
        # }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        session = RetroSession.objects.get()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'vote-reaction',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type': 'info',
            'message': message
        }))

    # async def connect(self):
    #     for key in self.scope.keys():
    #         print(key, self.scope[key])
    #     await self.accept()
        # await login(self.scope, user)
        # await database_sync_to_async(self.scope["session"].save)()

    async def disconnect(self, code):
        pass
