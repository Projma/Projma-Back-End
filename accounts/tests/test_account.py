from rest_framework import status
from conftest import USERNAME, EMAIL, PASSWORD
from accounts.models import Profile
import pytest


@pytest.mark.django_db
class TestCreateUser:

    class TestCreate:
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

    class TestExist:
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


@pytest.mark.django_db
class TestLoginUser:

    def test_login_valid_user_returns_200(self, create_user, login_user):
        create_user()
        response = login_user()
        assert response.status_code == status.HTTP_200_OK

    def test_login_invalid_user_returns_401(self, create_user, login_user):
        create_user(username='testuser1')
        response = login_user(username='testuser2')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_inactive_user_returns_401(self, create_user, login_user):
        create_user(is_active=False)
        response = login_user()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestProfile:
    def signup_and_signin_process(create_user, login_user, authenticate_user):
        create_user()
        response = login_user()
        assert response.status_code == status.HTTP_200_OK
        api_client = authenticate_user(response.data['access'])
        return api_client

    class TestGetProfile:
        def test_anonymous_user_get_profile_returns_401(self, api_client):
            response = api_client.get('/accounts/profile/myprofile/')
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        def test_authenticated_user_get_profile_returns_200(self, create_user, login_user, authenticate_user):
            api_client = TestProfile.signup_and_signin_process(create_user, login_user, authenticate_user)
            response = api_client.get('/accounts/profile/myprofile/')
            assert response.status_code == status.HTTP_200_OK
            assert response.data['user']['username'] == USERNAME

        def test_search_profile_returns_200(self, api_client, create_user):
            create_user()
            create_user(username='user2', email=EMAIL+'2')
            create_user(username='user3', email=EMAIL+'3')
            response = api_client.get(f'/accounts/profile/?search={USERNAME}')
            assert response.status_code == status.HTTP_200_OK
            assert len(response.data) == 1
            response = api_client.get(f'/accounts/profile/?search=user')
            assert response.status_code == status.HTTP_200_OK
            assert len(response.data) == 3

    class TestUpdateProfile:
        def test_authenticated_user_update_profile_returns_200(self, create_user, login_user, authenticate_user):
            api_client = TestProfile.signup_and_signin_process(create_user, login_user, authenticate_user)
            response = api_client.get('/accounts/profile/myprofile/')
            assert response.status_code == status.HTTP_200_OK
            assert response.data['bio'] is None
            response = api_client.patch('/accounts/profile/edit-myprofile/', {'bio': 'test bio'})
            assert response.status_code == status.HTTP_200_OK
            assert response.data['bio'] == 'test bio'

        def test_change_password_with_new_pass_returns_200(self, create_user, login_user, authenticate_user):
            api_client = TestProfile.signup_and_signin_process(create_user, login_user, authenticate_user)
            new_password = 'newpassword125411!@'
            response = api_client.post('/accounts/profile/change-password/', {'old_password': PASSWORD, 'new_password': new_password})
            assert response.status_code == status.HTTP_200_OK
            api_client.logout()
            response = login_user()
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
            response = login_user(password=new_password)
            assert response.status_code == status.HTTP_200_OK

        def test_change_password_with_incorrect_old_pass_returns_400(self, create_user, login_user, authenticate_user):
            api_client = TestProfile.signup_and_signin_process(create_user, login_user, authenticate_user)
            response = api_client.post('/accounts/profile/change-password/', {'old_password': 'wrongpasstest', 'new_password': PASSWORD})
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    class TestPublicProfile:
        def test_get_public_profile_user_exist_returns_200(self, create_user, login_user, authenticate_user):
            api_client = TestProfile.signup_and_signin_process(create_user, login_user, authenticate_user)
            response = api_client.get(f'/accounts/profile/public-profile/{USERNAME}/')
            assert response.status_code == status.HTTP_200_OK
            assert response.data['user']['username'] == USERNAME
            api_client.logout()
            response = api_client.get(f'/accounts/profile/public-profile/{USERNAME}/')
            assert response.status_code == status.HTTP_200_OK
            assert response.data['user']['username'] == USERNAME

        def test_get_public_profile_user_not_exist_returns_404(self, create_user, login_user, authenticate_user):
            api_client = TestProfile.signup_and_signin_process(create_user, login_user, authenticate_user)
            response = api_client.get(f'/accounts/profile/public-profile/testuser2/')
            assert response.status_code == status.HTTP_404_NOT_FOUND