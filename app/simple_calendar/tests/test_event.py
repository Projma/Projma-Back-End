from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from simple_calendar.models import Event
import pytest


@pytest.mark.django_db
class TestCreateEvent:
    def create_calendar_api(create_board, create_calendar, authenticated=True):
        response = create_board(authenticated=authenticated)
        if not authenticated:
            return response 
        board_id = response.data['id']
        return create_calendar(board_id)

#     def test_create_unauthorized_returns_401(self, create_board, create_calendar, create_event):
#         response = TestCreateEvent.create_calendar_api(create_board, create_calendar, authenticated=False)
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     def test_create_valid_event_returns_201(self, create_board, create_calendar, create_event):
#         response = TestCreateEvent.create_calendar_api(create_board, create_calendar)
#         assert response.status_code == status.HTTP_201_CREATED
        
#         calendar_id = response.data['id']
#         response = create_event(c_id=calendar_id)
#         assert response.status_code == status.HTTP_201_CREATED

#     def test_create_event_miss_required_fields_returns_400(self, create_board, create_calendar, create_event):
#         response = TestCreateEvent.create_calendar_api(create_board, create_calendar)
#         assert response.status_code == status.HTTP_201_CREATED
        
#         calendar_id = response.data['id']
#         response = create_event(calendar_id, title="")
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
        
#         response = create_event(calendar_id, time="")
#         assert response.status_code == status.HTTP_400_BAD_REQUEST

#     def test_create_event_without_any_type_returns_400(self, create_board, create_calendar, create_event):
#         response = TestCreateEvent.create_calendar_api(create_board, create_calendar)
#         assert response.status_code == status.HTTP_201_CREATED
        
#         calendar_id = response.data['id']
#         response = create_event(type="", custom_type="", c_id=calendar_id)
#         assert response.status_code == status.HTTP_400_BAD_REQUEST

#     def test_create_event_with_both_type_and_custom_type_returns_400(self, create_board, create_calendar, create_event):
#         response = TestCreateEvent.create_calendar_api(create_board, create_calendar)
#         assert response.status_code == status.HTTP_201_CREATED
        
#         calendar_id = response.data['id']
#         response = create_event(c_id=calendar_id, custom_type="tp")
#         assert response.status_code == status.HTTP_400_BAD_REQUEST

# @pytest.mark.django_db
# class TestUpdateEvent:
#     def test_update_event_returns_200(self, api_client:APIClient, create_board, create_calendar, create_event):
#         response = TestCreateEvent.create_calendar_api(create_board, create_calendar)
#         assert response.status_code == status.HTTP_201_CREATED
        
#         calendar_id = response.data['id']
#         response = create_event(c_id=calendar_id)
#         assert response.status_code == status.HTTP_201_CREATED
        
#         event_id = response.data['id']
#         url = reverse('event-detail', args=[event_id])
#         response = api_client.patch(url, {'title': 'new'})
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['title'] == 'new'

#     def test_update_both_type_and_custom_type_returns_400(self, api_client:APIClient, create_board, create_calendar, create_event):
#         response = TestCreateEvent.create_calendar_api(create_board, create_calendar)
#         assert response.status_code == status.HTTP_201_CREATED
        
#         calendar_id = response.data['id']
#         response = create_event(c_id=calendar_id)
#         assert response.status_code == status.HTTP_201_CREATED
        
#         event_id = response.data['id']
#         url = reverse('event-detail', args=[event_id])
#         response = api_client.patch(url, {'event_custom_type': 'holiday', 'event_type': 'ctype'})
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
        
#         response = api_client.patch(url, {'event_custom_type': '', 'event_type': ''})
#         assert response.status_code == status.HTTP_400_BAD_REQUEST

# @pytest.mark.django_db
# class TestRetrieveEvent:
#     def test_retrieve_event_returns_200(self, api_client:APIClient, create_board, create_calendar, create_event):
#         response = TestCreateEvent.create_calendar_api(create_board, create_calendar)
#         assert response.status_code == status.HTTP_201_CREATED
        
#         calendar_id = response.data['id']
#         response = create_event(calendar_id)
#         assert response.status_code == status.HTTP_201_CREATED
        
#         event_id = response.data['id']
#         url = reverse('event-detail', args=[event_id])
#         response = api_client.get(url)
        
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['calendar'] == calendar_id

# @pytest.mark.django_db
# class TestDeleteEvent:
#     def test_delete_exist_event_returns_204(self, api_client:APIClient, create_board, create_calendar, create_event):
#         response = TestCreateEvent.create_calendar_api(create_board, create_calendar)
#         assert response.status_code == status.HTTP_201_CREATED
        
#         calendar_id = response.data['id']
#         response = create_event(calendar_id)
#         assert response.status_code == status.HTTP_201_CREATED
#         assert Event.objects.count() == 1
        
#         event_id = response.data['id']
#         url = reverse('event-detail', args=[event_id])
#         response = api_client.delete(url)
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#         assert Event.objects.count() == 0