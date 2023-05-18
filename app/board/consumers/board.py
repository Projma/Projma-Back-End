import json
from channels.generic.websocket import WebsocketConsumer, async_to_sync
from channels.auth import login
from board.models import Board


class BoardConsumer(WebsocketConsumer):
    def connect(self):
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name
        # )
        self.USER = self.scope['user']
        self.accept()

        # self.send(json.dumps({
        #     'type': 'Test Message For Channel Connectivity',
        #     'message': 'Kosse nane chini KHARKOSDEH',
        # }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data = text_data_json['data']
        typ = text_data_json['type']

        if typ == 'join_board_group':
            response = self.join_board_group(data['board_id'])
            self.send(json.dumps({
                'type': 'join_board_group',
                'data': response
            }))

        else:
            async_to_sync(self.channel_layer.group_send)(
                self.BOARD_GROUP_NAME,
                {
                    'type': typ,
                    'data': data,
                    'sender_channel_name': self.channel_name
                }
            )

    def join_board_group(self, board_id):
        try:
            board = Board.objects.get(id=board_id)
        except:
            return {'code': 1, 'message': 'Board id is not valid'}
        if self.USER.profile not in board.members.all() | board.admins.all() \
                or self.USER.profile != board.workspace.owner:
            return {'code': 1, 'message': 'You dont have permission to access this board'}

        self.BOARD_GROUP = f'board_{board.id}'

        async_to_sync(self.channel_layer.group_add)(
            self.BOARD_GROUP,
            self.channel_name
        )
        return {'code': 0, 'message': 'Joined board group successfully'}

    def reorder_tasklists(self, event):
        print(event)
        if self.channel_name != event['sender_channel_name']:
            self.send(text_data=json.dumps(event))

    def reorder_tasks(self, event):
        if self.channel_name != event['sender_channel_name']:
            self.send(text_data=json.dumps(event))

    def create_tasklist(self, event):
        if self.channel_name != event['sender_channel_name']:
            self.send(text_data=json.dumps(event))

    def remove_tasklist(self, event):
        if self.channel_name != event['sender_channel_name']:
            self.send(text_data=json.dumps(event))

    async def disconnect(self, code):
        pass
