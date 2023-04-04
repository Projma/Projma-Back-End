import pytest
from datetime import datetime, time
from django.urls import reverse
from rest_framework.test import APIClient
from task.tests.conftest import *
from ..models import Event



class CalendarConf:
    def create_calendar(api_client:APIClient):
        def _create_calendar(b_id):
            url = reverse('calendar-list')
            return api_client.post(url, {'board': b_id})
        return _create_calendar


@pytest.fixture
def create_calendar(api_client:APIClient):
    def _create_calendar(b_id):
        return CalendarConf.create_calendar(api_client)(b_id)
    return _create_calendar
