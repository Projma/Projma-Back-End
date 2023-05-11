import pytest
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from retro.models import RetroSession, RetroCard, CardGroup
from accounts.models import Profile
=======
from retro.models import RetroSession
>>>>>>> 0c41274 ([feat]: start retro tests)
=======
from retro.models import RetroSession, RetroCard, CardGroup
from accounts.models import Profile
>>>>>>> 1d61429 ([feat]: add retro models)
=======
from retro.models import RetroSession
>>>>>>> 0c41274 ([feat]: start retro tests)
=======
from retro.models import RetroSession, RetroCard, CardGroup
from accounts.models import Profile
>>>>>>> 1d61429 ([feat]: add retro models)
=======
from retro.models import RetroSession
>>>>>>> 0c41274 ([feat]: start retro tests)
=======
from retro.models import RetroSession, RetroCard, CardGroup
from accounts.models import Profile
>>>>>>> 1d61429 ([feat]: add retro models)


@pytest.mark.django_db
class TestCreateRetroSession:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 1d61429 ([feat]: add retro models)
=======
>>>>>>> 1d61429 ([feat]: add retro models)
=======
>>>>>>> 1d61429 ([feat]: add retro models)
    def test_create_retro_session_success(self, create_board, create_account):
        # admin = Profile.objects.get(create_account().data['id'])
        # board = create_board()
        session = RetroSession.objects.create(board=None, admin=None)

    def test_create_retro_card_success(self):
        card = RetroCard.objects.create(text='card1', card_group=None)

    def test_create_retro_card_with_text_more_256_fails(self):
        text = '0123456789' * 100
        er = False
        try:
            card = RetroCard.objects.create(text=text, card_group=None)
        except:
            er = True
        assert er == True


    def test_create_card_group_success(self):
        session = RetroSession.objects.create(board=None, admin=None)
        cg = CardGroup.objects.create(retro_session=session, name='cardgroup1')
    def test_create_card_group_with_name_more_256_fails(self):
        session = RetroSession.objects.create(board=None, admin=None)
        er = False
        text = '0123456789' * 100
        try:
            cg = CardGroup.objects.create(retro_session=session, name=text)
        except:
            er = True
        assert er == True


    def test_retro_card_with_card_group(self):
        session = RetroSession.objects.create(board=None, admin=None)
        cg = CardGroup.objects.create(retro_session=session, name='cardgroup1')
        card = RetroCard.objects.create(card_group=cg, text='text')

    def test_retro_card_init_group(self):
        session = RetroSession.objects.create(board=None, admin=None)
        card = RetroCard.objects.create(card_group=None, text='text')
        # card.init_group(session.pk)
        # assert  card.card_group != None




<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
    def test_create_retro_session_success(self, create_board):
        board = create_board()
        # session = RetroSession.objects.create(board=None, attendees=[], admin=None)
>>>>>>> 0c41274 ([feat]: start retro tests)
=======
>>>>>>> 1d61429 ([feat]: add retro models)
=======
    def test_create_retro_session_success(self, create_board):
        board = create_board()
        # session = RetroSession.objects.create(board=None, attendees=[], admin=None)
>>>>>>> 0c41274 ([feat]: start retro tests)
=======
>>>>>>> 1d61429 ([feat]: add retro models)
=======
    def test_create_retro_session_success(self, create_board):
        board = create_board()
        # session = RetroSession.objects.create(board=None, attendees=[], admin=None)
>>>>>>> 0c41274 ([feat]: start retro tests)
=======
>>>>>>> 1d61429 ([feat]: add retro models)

