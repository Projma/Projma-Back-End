from rest_framework import status
from conftest import WORKSPACE_NAME, UserConf
from workspaces.models import WorkSpace
from accounts.models import Profile
import pytest


@pytest.mark.django_db
class TestCreateWorkspace:
    class TestAuthenticatedUser:
        def test_create_valid_workspace_returns_201(self, create_workspace):
            response = create_workspace()
            assert response.status_code == status.HTTP_201_CREATED

        def test_create_invalid_workspace_returns_400(self, create_workspace):
            response = create_workspace(name='')
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    class TestUnauthenticatedUser:
        def test_create_workspace_returns_401(self, create_workspace):
            response = create_workspace(authenticated=False)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUpdateWorkSpace:
    class TestIsOwner:
        def test_edit_workspace_returns_200(self, api_client, create_workspace):
            response = create_workspace()
            assert response.status_code == status.HTTP_201_CREATED
            assert response.data['name'] == WORKSPACE_NAME
            workspace_id = response.data['id']
            new_name = 'new_name'
            response = api_client.patch(f'/workspaces/workspaceowner/{workspace_id}/edit-workspace/', {'name': new_name})
            assert response.status_code == status.HTTP_200_OK
            assert response.data['name'] == new_name

    class TestIsMember:
        def test_edit_workspace_returns_403(self, api_client, create_account, create_workspace):
            response = create_workspace()
            assert response.status_code == status.HTTP_201_CREATED
            workspace_id = response.data['id']
            api_client = create_account(username='testuser2', password='testpassword2', email='testuser2@domain.com')
            new_name = 'new_name'
            response = api_client.patch(f'/workspaces/workspaceowner/{workspace_id}/edit-workspace/', {'name': new_name})
            assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestDeleteWorkSpace:
    class TestIsOwner:
        def test_delete_workspace_returns_204(self, api_client, create_workspace):
            response = create_workspace()
            assert response.status_code == status.HTTP_201_CREATED
            workspace_id = response.data['id']
            response = api_client.delete(f'/workspaces/workspaceowner/{workspace_id}/delete-workspace/')
            assert response.status_code == status.HTTP_204_NO_CONTENT

    class TestIsMember:
        def test_delete_workspace_returns_403(self, api_client, create_account, create_workspace):
            response = create_workspace()
            assert response.status_code == status.HTTP_201_CREATED
            workspace_id = response.data['id']
            api_client = create_account(username='testuser2', password='testpassword2', email='testuser2@domain.com')
            response = api_client.delete(f'/workspaces/workspaceowner/{workspace_id}/delete-workspace/')
            assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestWorkSpaceApis:
    class TestIsOwner:
        def test_get_invite_link_returns_200(self, api_client, create_workspace):
            response = create_workspace()
            assert response.status_code == status.HTTP_201_CREATED
            workspace_id = response.data['id']
            response = api_client.get(f'/workspaces/workspaceowner/{workspace_id}/invite-link/')
            assert response.status_code == status.HTTP_200_OK

        def test_add_user_to_workspace_returns_200(self, api_client, create_workspace):
            response = create_workspace()
            assert response.status_code == status.HTTP_201_CREATED
            workspace_id = response.data['id']
            workspace = WorkSpace.objects.filter(id=workspace_id).first()
            assert workspace.members.count() == 0
            user_response = UserConf.create_user(api_client)(username='testuser2', password='testpassword2', email='user2@domain.com' )
            user = Profile.objects.filter(user__username=user_response.data['username']).first().user
            response = api_client.post(f'/workspaces/workspaceowner/{workspace_id}/add-user-to-workspace/{user.id}/')
            assert response.status_code == status.HTTP_200_OK
            assert workspace.members.count() == 1

        def test_remove_user_from_workspace_returns_200(self, api_client, create_workspace):
            response = create_workspace()
            assert response.status_code == status.HTTP_201_CREATED
            workspace_id = response.data['id']
            workspace = WorkSpace.objects.filter(id=workspace_id).first()
            assert workspace.members.count() == 0
            user_response = UserConf.create_user(api_client)(username='testuser2', password='testpassword2', email='user2@domain.com')
            user = Profile.objects.filter(user__username=user_response.data['username']).first().user
            workspace.members.add(user.profile)
            workspace.save()
            assert workspace.members.count() == 1
            response = api_client.delete(f'/workspaces/workspaceowner/{workspace_id}/remove-user-from-workspace/{user.id}/')
            assert response.status_code == status.HTTP_200_OK
            assert workspace.members.count() == 0

    class TestIsMember:
        def test_get_invite_link_returns_403(self, api_client, create_account, create_workspace):
            response = create_workspace()
            assert response.status_code == status.HTTP_201_CREATED
            workspace_id = response.data['id']
            api_client = create_account(username='testuser2', password='testpassword2', email='testuser2@domain.com')
            response = api_client.get(f'/workspaces/workspaceowner/{workspace_id}/invite-link/')
            assert response.status_code == status.HTTP_403_FORBIDDEN

        def test_add_user_to_workspace_returns_403(self, api_client, create_account, create_workspace):
            response = create_workspace()
            assert response.status_code == status.HTTP_201_CREATED
            workspace_id = response.data['id']
            workspace = WorkSpace.objects.filter(id=workspace_id).first()
            assert workspace.members.count() == 0
            user_response = UserConf.create_user(api_client)(username='testuser2', password='testpassword2', email='user2@domain.com' )
            user_id = Profile.objects.filter(user__username=user_response.data['username']).first().user.id
            api_client = create_account(username='testuser3', password='testpassword3', email='user3@domain.com')
            response = api_client.post(f'/workspaces/workspaceowner/{workspace_id}/add-user-to-workspace/{user_id}/')
            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert workspace.members.count() == 0

        def test_remove_user_from_workspace_returns_403(self, api_client, create_account, create_workspace):
            response = create_workspace()
            assert response.status_code == status.HTTP_201_CREATED
            workspace_id = response.data['id']
            workspace = WorkSpace.objects.filter(id=workspace_id).first()
            assert workspace.members.count() == 0
            user_response = UserConf.create_user(api_client)(username='testuser2', password='testpassword2', email='user2@domain.com')
            user = Profile.objects.filter(user__username=user_response.data['username']).first().user
            workspace.members.add(user.profile)
            workspace.save()
            assert workspace.members.count() == 1
            api_client = create_account(username='testuser3', password='testpassword3', email='user3@domain.com')
            response = api_client.delete(f'/workspaces/workspaceowner/{workspace_id}/remove-user-from-workspace/{user.id}/')
            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert workspace.members.count() == 1