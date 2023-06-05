from rest_framework import status
import pytest

@pytest.mark.django_db
class TestCreateRetro:
    def test_create_retro_with_valid_board_returns_201(self, api_client, create_board, create_retro):
        response = create_board()
        board_id = response.data['id']
        retro = create_retro(board_id)
        print(response)
        assert response.status_code == status.HTTP_201_CREATED