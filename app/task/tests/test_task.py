from rest_framework import status
import pytest

@pytest.mark.django_db
class TestCreateTask:
    def test_create_valid_task_returns_201(self, create_board, create_tasklist, create_task):
        response = create_board()
        board_id = response.data['id']
        response = create_tasklist(board_id)
        tl_id = response.data['id']
        response =create_task(tl_id)
        assert response.status_code == status.HTTP_201_CREATED