import json
from django.db.models import Sum
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login
from retro.types import RetroSteps
from retro.models import RetroSession, RetroReaction, CardGroup

class VoteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.USER = self.scope['user']
        self.SESSION_ID = int(self.scope['url_route']['kwargs']['session_id'])
        self.GROUP_NAME = "session_%s" % self.SESSION_ID
        if not await self.check_accessability():
            await self.accept()
            await self.send(json.dumps({'code': 1, 'message': 'You do not have access to this session'}))
        else:
            await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
            await self.accept()
            await self.send(json.dumps({'code': 1, 'message': 'Connected successfully'}))

    @sync_to_async
    def check_accessability(self):
        board = RetroSession.objects.get(pk=self.SESSION_ID).board
        admin = board.admins.all()
        members = board.members.all()
        wowner = board.workspace.owner
        if (not self.USER.profile in (admin | members)) and self.USER.profile != wowner:
            return False
        return True

    @sync_to_async
    def update_limitation(self, val):
        retro_session = RetroSession.objects.get(pk=self.SESSION_ID)
        all_votes = RetroReaction.objects.filter(card_group__retro_session=retro_session)\
                        .aggregate(all_votes=Sum('count'))['all_votes']
        if retro_session.vote_limitation * retro_session.attendees.count() + val < all_votes:
            self.send(json.dumps({'code': 1, 'message': 'You can not decrease the vote limitation'}))
        elif retro_session.admin == self.USER.profile:
            retro_session.vote_limitation += val
            retro_session.save()
        else:
            self.send(json.dumps({'code': 1, 'message': 'You are not allowed to change the vote limitation'}))

    @sync_to_async
    def vote(self, cg_id, val):
        session = RetroSession.objects.get(pk=self.SESSION_ID)
        card_group = CardGroup.objects.get(pk=cg_id)
        reaction, is_created = RetroReaction.objects.get_or_create(card_group=card_group, reactor=self.USER.profile)
        if 0 <= reaction.count + val <= session.vote_limitation:
            reaction.count += val
            reaction.save()

    @sync_to_async
    def get_team_votes(self):
        session = RetroSession.objects.get(pk=self.SESSION_ID)
        team_votes = RetroReaction.objects.filter(card_group__retro_session=session)\
                        .aggregate(all_votes=Sum('count'))['all_votes']
        if not team_votes:
            team_votes = 0
        team_votes = session.vote_limitation * session.attendees.count() - team_votes
        return team_votes

    @sync_to_async
    def get_user_votes(self):
        session = RetroSession.objects.get(pk=self.SESSION_ID)
        user_votes = RetroReaction.objects.filter(card_group__retro_session=session).filter(reactor=self.USER.profile)\
                        .aggregate(all_votes=Sum('count'))['all_votes']
        if not user_votes:
            user_votes = 0
        user_votes = session.vote_limitation - user_votes
        return user_votes

    async def show_vote(self, event):
        user_votes = await self.get_user_votes()
        team_votes = await self.get_team_votes()
        await self.send(json.dumps({
            "user_votes": user_votes,
            "team_votes": team_votes
        }))

    async def receive(self, text_data):
        json_data = json.loads(text_data)
        request_type = json_data['type']
        if request_type == 'update_limitation':
            value = json_data['value']
            await self.update_limitation(value)
        elif request_type == 'vote':
            cg_id = json_data['card_group_id']
            value = json_data['value']
            await self.vote(cg_id, value)
        await self.channel_layer.group_send(self.GROUP_NAME,{
            'type': 'show_vote'
        })

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)
