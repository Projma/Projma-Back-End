from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User
from board.tests.conftest import *
from retro.models import *
import pytest

VOTE_LIMITATION = 5

class RetroConf:
    def create_retro(api_client:APIClient):
        def _create_retro(board_id, vote_limitation):
            # response = api_client.post('/retro/', {'board': board_id, 'vote_limitation': vote_limitation})
            board = Board.objects.get(pk=board_id)
            print('----------------', api_client.session)
            admin = Profile.objects.filter(pk=api_client.user).all()
            wowner = Profile.objects.filter(pk=board.workspace.owner).all()
            attendees = board.members.all() | board.admins.all() | wowner | admin
            retro = RetroSession.objects.create(board=board, attendees=attendees, admin=admin)
            return retro
        return _create_retro


@pytest.fixture
def create_retro(api_client: APIClient):
    def _create_retro(board_id, vote_limitation=VOTE_LIMITATION):
        return RetroConf.create_retro(api_client)(board_id, vote_limitation)
    return _create_retro