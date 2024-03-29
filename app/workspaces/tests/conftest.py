from rest_framework.test import APIClient
from accounts.models import User
import pytest

USERNAME = 'testuser'
PASSWORD = 'testpassword'
EMAIL = 'test@domain.com'
WORKSPACE_NAME = 'test_workspace'
WORKSPACE_TYPE = 'education'

class UserConf:
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

    def login_user(api_client:APIClient):
        def _login_user(username=USERNAME, password=PASSWORD):
            return api_client.post('/accounts/login/token/', {'username': username, 'password': password})
        return _login_user

    def authenticate_user(api_client:APIClient):
        def _authenticate_user(token):
            api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
            return api_client
        return _authenticate_user

    def create_account(api_client, username=USERNAME, password=PASSWORD, email=EMAIL, is_staff=False, is_superuser=False, is_active=True):
        UserConf.create_user(api_client)(username, password, email, is_staff, is_superuser, is_active)
        response = UserConf.login_user(api_client)(username, password)
        return UserConf.authenticate_user(api_client)(response.data['access'])


class WorkSpaceConf:
    def create_workspace(api_client:APIClient):
        def _create_workspace(name=WORKSPACE_NAME, type=WORKSPACE_TYPE, authenticated=True):
            client = UserConf.create_account(api_client)
            if not authenticated:
                client.credentials(HTT_AUTHORIZATION='')
            return client.post('/workspaces/dashboard/create-workspace/', {'name': name, 'type': type})
        return _create_workspace


@pytest.fixture
def create_account(api_client:APIClient):
    '''Creates a user, logs in, and returns an authenticated APIClient'''
    def _create_account(username=USERNAME, password=PASSWORD, email=EMAIL, is_staff=False, is_superuser=False, is_active=True):
        return UserConf.create_account(api_client, username, password, email, is_staff, is_superuser, is_active)
    return _create_account

@pytest.fixture
def create_workspace(api_client:APIClient):
    '''First creates an account then creates a workspace and returns the response(workspace object)'''
    def _create_workspace(name=WORKSPACE_NAME, type=WORKSPACE_TYPE, authenticated=True):
        return WorkSpaceConf.create_workspace(api_client)(name, type, authenticated)
    return _create_workspace

@pytest.fixture
def api_client():
    return APIClient()