import json
from channels.generic.websocket import WebsocketConsumer, async_to_sync
from channels.auth import login


class BoardConsumer(WebsocketConsumer):
    def connect(self):
        # self.room_group_name = 'X'
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name
        # )
        self.accept()

        self.send(json.dumps({
            'type': 'Test Message For Channel Connectivity',
            'message': 'Kire Khar :/',
        }))

    # async def connect(self):
    #     for key in self.scope.keys():
    #         print(key, self.scope[key])
    #     await self.accept()
        # await login(self.scope, user)
        # await database_sync_to_async(self.scope["session"].save)()

    async def disconnect(self, code):
        pass
