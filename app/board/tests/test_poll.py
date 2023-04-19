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

