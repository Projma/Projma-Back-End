from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
class TestCreateCalendar:
    def test_valid_board_create_calendar_returns_201(self, create_board, create_calendar):
        response = create_board()
        board_id = response.data['id']
        response = create_calendar(board_id)
        
        assert response.status_code == status.HTTP_201_CREATED

    def test_invalid_board_create_calendar_returns_400(self, create_board, create_calendar):
        response = create_board()
        board_id = response.data['id']
        response = create_calendar(board_id + 1)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_authenticated_create_calendar_returns_201(self, create_board, create_calendar):
        response = create_board()

        assert response.status_code == status.HTTP_201_CREATED
        
        board_id = response.data['id']
        response = create_calendar(board_id)
        
        assert response.status_code == status.HTTP_201_CREATED

    def test_unauthenticated_create_calendar_returns_401(self, create_board, create_calendar):
        response = create_board(authenticated=False)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestDeleteCalendar:
    def test_delete_exist_calendar_returns_204(self, api_client:APIClient, create_board, create_calendar):
        response = create_board()
        board_id = response.data['id']
        response = create_calendar(board_id)
        
        assert response.status_code == status.HTTP_201_CREATED
        
        calendar_id = response.data['id']
        url = reverse('calendar-detail', args=[calendar_id])
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_invalid_calendar_returns_400(self, api_client:APIClient, create_board, create_calendar):
        response = create_board()
        board_id = response.data['id']
        response = create_calendar(board_id)
        
        assert response.status_code == status.HTTP_201_CREATED
        
        calendar_id = response.data['id']
        url = reverse('calendar-detail', args=[calendar_id + 1])
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND