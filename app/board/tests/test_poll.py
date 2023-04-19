from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
class TestCreatePoll:
    def test_create_valid_poll_returns_201(self, create_board, create_poll):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED

        board_id = response.data['id']
        response = create_poll(board_id)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_invalid_poll_returns_400(self, create_board, create_poll):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED

        board_id = response.data['id']
        response = create_poll(board_id, question='')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeletePoll:
    def test_delete_exist_poll_returns_204(self, create_board, create_poll, api_client):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED

        board_id = response.data['id']
        response = create_poll(board_id)
        assert response.status_code == status.HTTP_201_CREATED

        poll_id = response.data['id']
        url = reverse('poll-detail', args=[poll_id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_invalid_poll_returns_400(self, create_board, create_poll, api_client):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED

        board_id = response.data['id']
        response = create_poll(board_id)
        assert response.status_code == status.HTTP_201_CREATED

        poll_id = response.data['id']
        url = reverse('poll-detail', args=[poll_id+1])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateAnswer:
    def test_create_valid_answer_returns_201(self, create_board, create_poll, create_answer):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED

        board_id = response.data['id']
        response = create_poll(board_id)
        assert response.status_code == status.HTTP_201_CREATED

        poll_id = response.data['id']
        response = create_answer(poll_id)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_invalid_answer_returns_400(self, create_board, create_poll, create_answer):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED

        board_id = response.data['id']
        response = create_poll(board_id)
        assert response.status_code == status.HTTP_201_CREATED

        poll_id = response.data['id']
        response = create_answer(poll_id, text='')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


