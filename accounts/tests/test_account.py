from rest_framework import status
from conftest import USERNAME, EMAIL, PASSWORD
from accounts.models import Profile
import pytest


@pytest.mark.django_db
class TestCreateUser:

    def test_create_valid_user_returns_201(self, create_user):
        response = create_user()
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == USERNAME

    def test_create_invalid_user_returns_400(self, create_user):
        response = create_user(username='', password='', email='')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_check_profile_created_while_creating_user(self, create_user):
        response = create_user()
        assert response.status_code == status.HTTP_201_CREATED
        assert Profile.objects.filter(user__username=USERNAME).exists()

    def test_check_username_exists_returns_400(self, create_user):
        response1 = create_user(username=USERNAME)
        response2 = create_user(username=USERNAME)
        assert response1.status_code == status.HTTP_201_CREATED
        assert response2.status_code == status.HTTP_400_BAD_REQUEST

    def test_check_email_exists_returns_400(self, create_user):
        response1 = create_user(email=EMAIL)
        response2 = create_user(email=EMAIL)
        assert response1.status_code == status.HTTP_201_CREATED
        assert response2.status_code == status.HTTP_400_BAD_REQUEST

