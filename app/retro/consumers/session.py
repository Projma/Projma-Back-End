import json
from channels.generic.websocket import WebsocketConsumer, async_to_sync
from channels.auth import login
from retro.types import RetroSteps
from retro.models import RetroSession


class SessionConsumer(WebsocketConsumer):
    def connect(self):
        self.USER = self.scope['user']
        self.SESSION_ID = self.scope['url_route']['kwargs']['session_id']
        self.GROUP_NAME = "session_%s" % self.SESSION_ID
        async_to_sync(self.channel_layer.group_add)(self.GROUP_NAME, self.channel_name)
        self.accept()

    def session_next(self, event):
        print('################')
        session = event['session']
        session.retro_step = RetroSteps.next(session.retro_step)
        session.save()
        self.send(text_data=json.dumps({'session': session}))
        return {'session': session}

    def receive(self, text_data):
        print(self.groups)
        json_data = json.loads(text_data)
        if json_data['type'] == 'session_next':
            try:
                session = RetroSession.objects.get(pk=self.SESSION_ID)
            except:
                return {
                    'code': 1,
                    'message': 'The session is invalid'
                }
            print("Before--------")
            async_to_sync(self.channel_layer.group_send)(
                self.GROUP_NAME,
                {
                    'type': 'session_next',
                    'data': session,
                    'sender_channel_name': self.channel_name
                }
            )
            print("After--------")

    def disconnect(self, code):
        print(code, 'disconnecting........')
        self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)