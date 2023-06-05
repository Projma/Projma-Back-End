from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User
from board.tests.conftest import *
from retro.models import *
import pytest

VOTE_LIMITATION = 5

class RetroConf:
    def create_retro(api_client:APIClient):
        def _create_retro(vote_limitation):
            response = BoardConf.create_board(api_client)()
            board = Board.objects.get(pk=response.data['id'])
            admin = Profile.objects.filter(user__username=USERNAME).all()
            wowner = Profile.objects.filter(pk=board.workspace.owner).all()
            attendees = board.members.all() | board.admins.all() | wowner | admin
            retro = RetroSession.objects.create(board=board, admin=admin.first(), vote_limitation=VOTE_LIMITATION)
            retro.attendees.set(attendees)
            retro.save()
            return retro
        return _create_retro


@pytest.fixture
def create_retro(api_client: APIClient):
    def _create_retro(vote_limitation=VOTE_LIMITATION):
        return RetroConf.create_retro(api_client)(vote_limitation)
    return _create_retro