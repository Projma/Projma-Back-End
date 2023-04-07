from rest_framework import status
from board.models import TaskList
from .conftest import TASKLIST_NAME
import pytest


@pytest.mark.django_db
class TestCreateTaskList:
    def test_create_valid_tasklist_returns_201(self, create_board, create_tasklist):
        response = create_board()
        board_id = response.data['id']
        response = create_tasklist(board_id)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_invalid_tasklist_returns_400(self, create_board, create_tasklist):
        response = create_board()
        board_id = response.data['id']
        response = create_tasklist(board_id, title='')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUpdateTaskList:
    def test_update_tasklist_returns_200(self, api_client, create_board, create_tasklist):
        response = create_board()
        board_id = response.data['id']
        response = create_tasklist(board_id)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == TASKLIST_NAME
        tasklist_id = response.data['id']
        # response = api_client.patch(f'/workspaces/tasklist/{tasklist_id}/update-tasklist/', data={'title': 'New Title'})
        response = api_client.patch(f'/board/tasklist/{tasklist_id}/update-tasklist/', data={'title': 'New Title'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'New Title'


@pytest.mark.django_db
class TestDeleteTaskList:
    def test_delete_tasklist_returns_204(self, api_client, create_board, create_tasklist):
        response = create_board()
        board_id = response.data['id']
        response = create_tasklist(board_id)
        tasklist_id = response.data['id']
        tasklist = TaskList.objects.filter(pk=tasklist_id)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(tasklist) == 1
        # response = api_client.delete(f'/workspaces/tasklist/{tasklist_id}/delete-tasklist/')
        response = api_client.delete(f'/board/tasklist/{tasklist_id}/delete-tasklist/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        tasklist = TaskList.objects.filter(pk=tasklist_id)
        assert len(tasklist) == 0


@pytest.mark.django_db
class TestBoardTaskLists:
    def test_get_board_tasklists_returns_200(self, api_client, create_board, create_tasklist):
        response = create_board()
        board_id = response.data['id']
        response1 = create_tasklist(board_id, title='TaskList 1')
        assert response1.status_code == status.HTTP_201_CREATED
        response2 = create_tasklist(board_id, title='TaskList 2')
        assert response2.status_code == status.HTTP_201_CREATED
        # response = api_client.get(f'/workspaces/board/{board_id}/get-board-tasklists/')
        response = api_client.get(f'/board/{board_id}/get-board-tasklists/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2