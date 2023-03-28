from rest_framework.test import APIClient
from accounts.models import User
import pytest

USERNAME = 'testuser'
PASSWORD = 'testpassword'
EMAIL = 'test@domain.com'

@pytest.fixture
def create_user(api_client):
    def _create_user(username=USERNAME, password=PASSWORD, email=EMAIL, is_staff=False, is_superuser=False, is_active=True):
        response = api_client.post('/accounts/users/signup/', {'username': username, 'password': password, 'email': email})
        user = User.objects.filter(username=username).first()
        if user:
            user.is_active = is_active
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save()
        return response
    return _create_user

@pytest.fixture
def login_user(api_client:APIClient):
    def _login_user(username=USERNAME, password=PASSWORD):
        return api_client.post('/accounts/login/token/', {'username': username, 'password': password})
    return _login_user

@pytest.fixture
def authenticate_user(api_client:APIClient):
    def _authenticate_user(token):
        api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        return api_client
    return _authenticate_user

@pytest.fixture
def api_client():
    return APIClient()