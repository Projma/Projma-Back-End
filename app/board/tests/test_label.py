from rest_framework import status
from board.models import Board
import pytest

@pytest.mark.django_db
class TestCreateLabel:
    def test_create_valid_label_returns_201(self, api_client, create_board):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED
        board_id = response.data['id']
        response = api_client.post(f'/workspaces/board/{board_id}/create-label/', {'title': 'test label', 'color': '#000000'})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'test label'

    def test_create_invalid_label_returns_400(self, api_client, create_board):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED
        board_id = response.data['id']
        response = api_client.post(f'/workspaces/board/{board_id}/create-label/', {'title': '', 'color': '#000000'})
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUpdateLabel:
    def test_update_board_returns_200(self, api_client, create_board):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED
        board_id = response.data['id']
        response = api_client.post(f'/workspaces/board/{board_id}/create-label/', {'title': 'test label', 'color': '#000000'})
        assert response.status_code == status.HTTP_201_CREATED
        label_id = response.data['id']
        new_title = 'new_title'
        response = api_client.patch(f'/workspaces/label/{label_id}/update-label/', {'title': new_title})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == new_title


@pytest.mark.django_db
class TestDeleteLabel:
    def test_delete_label_returns_204(self, api_client, create_board):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED
        board_id = response.data['id']
        response = api_client.post(f'/workspaces/board/{board_id}/create-label/', {'title': 'test label', 'color': '#000000'})
        assert response.status_code == status.HTTP_201_CREATED
        label_id = response.data['id']
        response = api_client.delete(f'/workspaces/label/{label_id}/delete-label/')
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestBoardLabels:
    def test_get_board_labels_returns_200(self, api_client, create_board):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED
        board_id = response.data['id']
        board = Board.objects.filter(pk=board_id).first()
        assert board.labels.count() == 0
        response = api_client.post(f'/workspaces/board/{board_id}/create-label/', {'title': 'test label', 'color': '#000000'})
        assert response.status_code == status.HTTP_201_CREATED
        assert board.labels.count() == 1
        response = api_client.get(f'/workspaces/board/{board_id}/get-board-labels/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1