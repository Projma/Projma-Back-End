from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User
import pytest

USERNAME = 'testuser'
PASSWORD = 'testpassword'
EMAIL = 'test@domain.com'
WORKSPACE_NAME = 'test_workspace'
WORKSPACE_TYPE = 'education'
BOARD_NAME = 'test_board'
TASKLIST_NAME = 'test_tasklist'
POLL_QUESTION = 'Question'
POLL_ANSWER_TEXT = 'Text'

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


class BoardConf:
    def create_board(api_client:APIClient):
        def _create_board(name=BOARD_NAME, authenticated=True, admins=[], members=[]):
            client = UserConf.create_account(api_client)
            if not authenticated:
                client.credentials(HTT_AUTHORIZATION='')
            workspace_response = WorkSpaceConf.create_workspace(client)(authenticated=authenticated)
            if workspace_response.status_code == 201:
                workspace_id = workspace_response.data['id']
                return client.post(f'/workspaces/workspaceowner/{workspace_id}/create-board/', {'name': name, 'admins': admins, 'members': members})
            return workspace_response
        return _create_board


class TaskListConf:
    def create_tasklist(api_client:APIClient):
        def _create_tasklist(board_id, title=TASKLIST_NAME):
            # return api_client.post(f'/workspaces/board/{board_id}/create-tasklist/', {'title': title})
            return api_client.post(f'/board/tasklist/{board_id}/create-tasklist/', {'title': title})
        return _create_tasklist


class PollConf:
    def create_poll(api_client:APIClient):
        def _create_poll(board_id, question=POLL_QUESTION, is_open=True, is_multianswer=False, is_known=True):
            url = reverse('poll-list')
            return api_client.post(url, {'board': board_id, 'question': question, 'is_open': is_open, 'is_multianswer': is_multianswer, 'is_known': is_known})
        return _create_poll

    def create_answer(api_client:APIClient):
        def _create_answer(poll_id, text=POLL_ANSWER_TEXT, order=1):
            url = reverse('poll-answers-list')
            return api_client.post(url, {'poll': poll_id, 'text': text, 'order': order})
        return _create_answer


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
def create_board(api_client:APIClient):
    '''First creates an account then creates a workspace then creates a board and returns the response(board object)'''
    def _create_board(name=BOARD_NAME, authenticated=True):
        return BoardConf.create_board(api_client)(name, authenticated)
    return _create_board

@pytest.fixture
def create_tasklist(api_client:APIClient):
    '''you should create board first then call it. it returns the response(tasklist object)'''
    def _create_tasklist(board_id, title=TASKLIST_NAME):
        return TaskListConf.create_tasklist(api_client)(board_id, title)
    return _create_tasklist

@pytest.fixture
def create_poll(api_client:APIClient):
    '''you should create board first then call it. it returns the response(poll object)'''
    def _create_poll(board_id, question=POLL_QUESTION, is_open=True, is_multianswer=False, is_known=True):
        return PollConf.create_poll(api_client)(board_id, question, is_open, is_multianswer, is_known)
    return _create_poll

@pytest.fixture
def create_answer(api_client:APIClient):
    '''you should create board then create poll after that call it. it returns the response(pollanswer object)'''
    def _create_answer(poll_id, text=POLL_ANSWER_TEXT, order=1):
        return PollConf.create_answer(api_client)(poll_id, text, order)
    return _create_answer

@pytest.fixture
def api_client():
    return APIClient()