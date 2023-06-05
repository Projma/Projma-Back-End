from rest_framework import status
import pytest

@pytest.mark.django_db
class TestCreateTask:
    def create_task(create_board, create_tasklist, create_task):
        response = create_board()
        board_id = response.data['id']
        response = create_tasklist(board_id)
        tl_id = response.data['id']
        response =create_task(tl_id)
        return response

    def test_create_valid_task_returns_201(self, create_board, create_tasklist, create_task):
        response = TestCreateTask.create_task(create_board, create_tasklist, create_task)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_invalid_task_returns_404(self, create_board, create_tasklist, create_task):
        response = create_board()
        board_id = response.data['id']
        response = create_tasklist(board_id)
        tl_id = response.data['id']
        response =create_task(tl_id+1)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestGetTask:
    def test_get_valid_task_returns_200(self, api_client, create_board, create_tasklist, create_task):
        response = TestCreateTask.create_task(create_board, create_tasklist, create_task)
        task_id = response.data['id']
        response = api_client.get(f'/task/{task_id}/get-task/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == task_id

    def test_get_invalid_task_returns_404(self, api_client, create_board, create_tasklist, create_task):
        response = TestCreateTask.create_task(create_board, create_tasklist, create_task)
        task_id = response.data['id']
        response = api_client.get(f'/task/{task_id+1}/get-task/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
