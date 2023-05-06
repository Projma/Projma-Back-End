import pytest
from retro.models import RetroSession


@pytest.mark.django_db
class TestCreateRetroSession:
    def test_create_retro_session_success(self, create_board):
        board = create_board()
        # session = RetroSession.objects.create(board=None, attendees=[], admin=None)

