from rest_framework import status
from workspaces.models import Board
import pytest


@pytest.mark.django_db
class TestCreateBoard:
    def test_create_valid_board_returns_201(self, create_board):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_invalid_board_returns_400(self, create_board):
        response = create_board(name='')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUpdateBoard:
    def test_update_board_returns_200(self, api_client, create_board):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED
        board_id = response.data['id']
        new_name = 'new_name'
        response = api_client.patch(f'/workspaces/boardsadminapi/{board_id}/edit-board/', {'name': new_name})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == new_name


@pytest.mark.django_db
class TestDeleteBoard:
    def test_delete_board_returns_204(self, api_client, create_board):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED
        board_id = response.data['id']
        response = api_client.delete(f'/workspaces/boardsadminapi/{board_id}/delete-board/')
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestJoinBoard:
    def test_board_invite_link_returns_200(self, api_client, create_board):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED
        board_id = response.data['id']
        response = api_client.get(f'/workspaces/board/{board_id}/invite_link/')
        assert response.status_code == status.HTTP_200_OK

    def test_board_new_user_join_with_invite_link_returns_200(self, api_client, create_account, create_board):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED
        board_id = response.data['id']
        board = Board.objects.filter(id=board_id).first()
        assert board.members.count() == 0
        response = api_client.get(f'/workspaces/board/{board_id}/invite_link/')
        assert response.status_code == status.HTTP_200_OK
        invite_link = response.data
        api_client = create_account(username='newuser', password='newpassword64655gf51', email='newuser@domain.com')
        response = api_client.post(f'/workspaces/board/join-to-board/{invite_link}/')
        assert response.status_code == status.HTTP_200_OK
        assert board.members.count() == 1

    def test_board_existing_user_join_with_invite_link_returns_400(self, api_client, create_account, create_board):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED
        board_id = response.data['id']
        board = Board.objects.filter(id=board_id).first()
        assert board.members.count() == 0
        response = api_client.get(f'/workspaces/board/{board_id}/invite_link/')
        assert response.status_code == status.HTTP_200_OK
        invite_link = response.data
        response = api_client.post(f'/workspaces/board/join-to-board/{invite_link}/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_board_join_with_invalid_invite_link_returns_404(self, api_client, create_account, create_board):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED
        board_id = response.data['id']
        board = Board.objects.filter(id=board_id).first()
        assert board.members.count() == 0
        response = api_client.get(f'/workspaces/board/{board_id}/invite_link/')
        assert response.status_code == status.HTTP_200_OK
        invite_link = response.data + 'A'
        api_client = create_account(username='newuser', password='newpassword64655gf51', email='newuser@domain.com')
        response = api_client.post(f'/workspaces/board/join-to-board/{invite_link}/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
