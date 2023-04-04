from datetime import datetime, timedelta, date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from simple_calendar.tests.test_event import TestCreateEvent
from simple_calendar.models import Event
import pytest


now = datetime.now()
DAY = 1
WEEK = 7
MONTH = 30

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


@pytest.mark.django_db
class TestCalendarEvents:
    def test_events_with_once_occurrence_returns_200(self, api_client:APIClient, create_board, create_calendar, create_event):
        response = TestCreateEvent.create_calendar_api(create_board, create_calendar)
        assert response.status_code == status.HTTP_201_CREATED
        
        calendar_id = response.data['id']
        response = create_event(calendar_id, title='e1', duration=0, time=datetime(now.year, now.month, 5))
        assert response.status_code == status.HTTP_201_CREATED
        response = create_event(calendar_id, title='e2', duration=0, time=datetime(now.year, now.month, 10))
        assert response.status_code == status.HTTP_201_CREATED
        response = create_event(calendar_id, title='e3', duration=0, time=datetime(now.year, now.month, 17))
        assert response.status_code == status.HTTP_201_CREATED
        assert Event.objects.count() == 3
        
        start = f'{now.year}-{now.month}-{1} {00}:{00}:{00}'
        end = f'{now.year}-{now.month}-{MONTH} {23}:{59}:{59}'
        url = reverse('calendar-events', args=[calendar_id]) + f'?start={start}&end={end}'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3
        
        start = f'{now.year}-{now.month}-{WEEK} {00}:{00}:{00}'
        end = f'{now.year}-{now.month}-{2*WEEK} {23}:{59}:{59}'
        url = reverse('calendar-events', args=[calendar_id]) + f'?start={start}&end={end}'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        
        start = f'{now.year}-{now.month}-{10} {00}:{00}:{00}'
        end = f'{now.year}-{now.month}-{20} {23}:{59}:{59}'
        url = reverse('calendar-events', args=[calendar_id]) + f'?start={start}&end={end}'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_events_with_more_than_once_occurrence_returns_200(self, api_client:APIClient, create_board, create_calendar, create_event):
        response = TestCreateEvent.create_calendar_api(create_board, create_calendar)
        assert response.status_code == status.HTTP_201_CREATED
        
        calendar_id = response.data['id']
        response = create_event(calendar_id, title='e1', duration=DAY, time=datetime(now.year, 6, 5))
        assert response.status_code == status.HTTP_201_CREATED
        response = create_event(calendar_id, title='e2', duration=WEEK, time=datetime(now.year, 6, 10))
        assert response.status_code == status.HTTP_201_CREATED
        response = create_event(calendar_id, title='e3', duration=2, time=datetime(now.year, 6, 17))
        assert response.status_code == status.HTTP_201_CREATED
        response = create_event(calendar_id, title='e4', duration=0, time=datetime(now.year, 6 + 1, 2))
        assert response.status_code == status.HTTP_201_CREATED
        assert Event.objects.count() == 4
        
        start = f'{now.year}-{6}-{1} {00}:{00}:{00}'
        end = f'{now.year}-{6}-{MONTH} {23}:{59}:{59}'
        url = reverse('calendar-events', args=[calendar_id]) + f'?start={start}&end={end}'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 26 + 3 + 7
        
        start = f'{now.year}-{6}-{15} {00}:{00}:{00}'
        end = f'{now.year}-{6}-{30} {23}:{59}:{59}'
        url = reverse('calendar-events', args=[calendar_id]) + f'?start={start}&end={end}'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 16 + 2 + 7
        
        start = f'{now.year}-{6}-{15} {00}:{00}:{00}'
        end = f'{now.year}-{6+1}-{15} {23}:{59}:{59}'
        url = reverse('calendar-events', args=[calendar_id]) + f'?start={start}&end={end}'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 31 + 5 + 15 + 1

    def test_events_with_tasks_returns_200(self, api_client:APIClient, create_board, create_calendar, create_event, create_tasklist, create_task):
        response = TestCreateEvent.create_calendar_api(create_board, create_calendar)
        board_id = response.data['board']
        assert response.status_code == status.HTTP_201_CREATED
        
        calendar_id = response.data['id']
        response = create_event(calendar_id, title='e1', duration=DAY, time=datetime(now.year, 6, 5))
        assert response.status_code == status.HTTP_201_CREATED
        response = create_event(calendar_id, title='e2', duration=WEEK, time=datetime(now.year, 6, 10))
        assert response.status_code == status.HTTP_201_CREATED
        response = create_event(calendar_id, title='e3', duration=2, time=datetime(now.year, 6, 17))
        assert response.status_code == status.HTTP_201_CREATED
        response = create_event(calendar_id, title='e4', duration=0, time=datetime(now.year, 6 + 1, 2))
        assert response.status_code == status.HTTP_201_CREATED
        assert Event.objects.count() == 4
        
        response = create_tasklist(board_id)
        tl_id = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        
        response = create_task(tl_id, title='t1', start_date=date(now.year, 6, 12), end_date=date(now.year, 6, 24))
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['end_date'] != None
        response = create_task(tl_id, title='t2', end_date=date(now.year, 7, 7), start_date=date(now.year, 6, 26))
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['end_date'] != None
        
        start = f'{now.year}-{6}-{1} {00}:{00}:{00}'
        end = f'{now.year}-{6}-{MONTH} {23}:{59}:{59}'
        url = reverse('calendar-events', args=[calendar_id]) + f'?start={start}&end={end}'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 26 + 3 + 7 + 1
        
        start = f'{now.year}-{7}-{1} {00}:{00}:{00}'
        end = f'{now.year}-{7}-{MONTH} {23}:{59}:{59}'
        url = reverse('calendar-events', args=[calendar_id]) + f'?start={start}&end={end}'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 30 + 5 + 15 + 1 + 1
