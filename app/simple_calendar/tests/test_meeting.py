from datetime import datetime, time, date, timedelta
from simple_calendar.models import Meeting
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from simple_calendar.models import Event
import pytest

@pytest.mark.django_db
class TestCreateMeeting:
    def create_calendar_api(self, create_board, create_calendar, authenticated=True):
        response = create_board(authenticated=authenticated)
        if not authenticated:
            return response
        board_id = response.data['id']
        return create_calendar(board_id)

    def test_create_valid_meeting_returns_201(self, create_board, create_calendar, create_meeting):
        response = self.create_calendar_api(create_board, create_calendar)
        assert response.status_code == status.HTTP_201_CREATED

        response = create_meeting(response.data['id'])
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_meeting_with_invalid_time_returns_400(self, create_board, create_calendar, create_meeting):
        response = self.create_calendar_api(create_board, create_calendar)
        assert response.status_code == status.HTTP_201_CREATED

        start = time(12, 0, 0)
        end = time(11, 0, 0)
        response = create_meeting(response.data['id'], start=start, end=end)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_meeting_with_invalid_date_returns_400(self, create_board, create_calendar, create_meeting):
        response = self.create_calendar_api(create_board, create_calendar)
        assert response.status_code == status.HTTP_201_CREATED

        from_date = datetime(2020, 2, 2, 1, 1, 1).date()
        until_date = datetime(2020, 1, 1, 1, 1, 1).date()
        response = create_meeting(response.data['id'], from_date=from_date, until_date=until_date)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_meeting_with_invalid_repeat_returns_400(self, create_board, create_calendar, create_meeting):
        response = self.create_calendar_api(create_board, create_calendar)
        assert response.status_code == status.HTTP_201_CREATED

        from_date = datetime(2020, 2, 2, 1, 1, 1).date()
        until_date = datetime(2020, 3, 3, 1, 1, 1).date()
        repeat=0
        response = create_meeting(response.data['id'], from_date=from_date, until_date=until_date, repeat=0)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_start_meeting_before_start_time_returns_400(self, create_board, create_calendar, create_meeting, start_meeting):
        response = self.create_calendar_api(create_board, create_calendar)
        assert response.status_code == status.HTTP_201_CREATED
        start = (datetime.now() + timedelta(minutes=10)).time()
        end = (datetime.now() + timedelta(minutes=10)).time()
        response = create_meeting(response.data['id'], start=start, end=end)
        assert response.status_code == status.HTTP_201_CREATED

        response = start_meeting(m_id=response.data['id'])
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_start_meeting_before_from_date_returns_400(self, create_board, create_calendar, create_meeting, start_meeting):
        response = self.create_calendar_api(create_board, create_calendar)
        assert response.status_code == status.HTTP_201_CREATED
        from_date = (datetime.now() + timedelta(days=2)).date()
        until_date = (datetime.now() + timedelta(days=2)).date()
        response = create_meeting(response.data['id'], from_date=from_date, until_date=until_date)
        assert response.status_code == status.HTTP_201_CREATED

        response = start_meeting(m_id=response.data['id'])
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_start_holding_meeting_returns_400(self, create_board, create_calendar, create_meeting, start_meeting):
        response = self.create_calendar_api(create_board, create_calendar)
        assert response.status_code == status.HTTP_201_CREATED
        response = create_meeting(response.data['id'])
        assert response.status_code == status.HTTP_201_CREATED
        meet_id = response.data['id']
        meet = Meeting.objects.get(id=meet_id)
        meet.status = Meeting.HOLDING
        meet.save()

        response = start_meeting(m_id=meet_id)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_start_finished_meeting_returns_400(self, create_board, create_calendar, create_meeting, start_meeting):
        response = self.create_calendar_api(create_board, create_calendar)
        assert response.status_code == status.HTTP_201_CREATED
        response = create_meeting(response.data['id'])
        assert response.status_code == status.HTTP_201_CREATED
        meet_id = response.data['id']
        meet = Meeting.objects.get(id=meet_id)
        meet.status = Meeting.FINISHED
        meet.save()

        response = start_meeting(m_id=meet_id)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

