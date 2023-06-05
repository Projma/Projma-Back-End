from rest_framework import status
from .conftest import VOTE_LIMITATION, USERNAME
from retro.models import RetroSession
import pytest

@pytest.mark.django_db
class TestCreateRetro:
    def test_create_retro(self, api_client, create_retro):
        retro = create_retro()
        assert retro.vote_limitation == VOTE_LIMITATION
        assert retro.admin.user.username == USERNAME


@pytest.mark.django_db
class TestGetRetro:
    def test_get_valid_retro_returns_200(self, api_client, create_retro):
        retro = create_retro()
        response = api_client.get(f'/retro/{retro.pk}/')
        assert response.data['id'] > 0
        assert response.status_code == status.HTTP_200_OK

    def test_get_invalid_retro_returns_404(self, api_client, create_retro):
        retro = create_retro()
        response = api_client.get(f'/retro/{retro.pk+1}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteRetro:
    def test_delete_valid_retro_returns_204(self, api_client, create_retro):
        retro = create_retro()
        response = api_client.delete(f'/retro/{retro.pk}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        retro_cnt = RetroSession.objects.filter(pk=retro.pk).count()
        assert retro_cnt == 0

    def test_delete_invalid_retro_returns_404(self, api_client, create_retro):
        retro = create_retro()
        response = api_client.delete(f'/retro/{retro.pk+1}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND