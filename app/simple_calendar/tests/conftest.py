import pytest
from datetime import datetime
from django.urls import reverse
from rest_framework.test import APIClient
from task.tests.conftest import *
from simple_calendar.models import Event


now = datetime.now()
EVENT_TITLE = "event_1"
EVENT_TIME = datetime(now.year, now.month, now.day, 23, 59, 59)
EVENT_DURATION = 7
EVENT_COLOR = '#B253b2'
EVENT_TYPES = [x[0] for x in Event.EVENT_TYPE_CHOICES]
CUSTOM_TYPE = ""

MEETING_TITLE = "meeting_1"
MEETING_DESCRIPTION = 'meeting_description'
MEETING_START = datetime.now().time()
MEETING_END = datetime.now().time()
MEETING_FROM_DATE = datetime(now.year, now.month, now.day, 23, 59, 59).date()
MEETING_UNTIL_DATE = MEETING_FROM_DATE
MEETING_REPEAT = 0
MEETING_COLOR = '#222222'

class CalendarConf:
    def create_calendar(api_client:APIClient):
        def _create_calendar(b_id):
            url = reverse('calendar-list')
            return api_client.post(url, {'board': b_id})
        return _create_calendar

class EventConf:
    def create_event(api_client:APIClient):
        def _create_event(c_id, title=EVENT_TITLE, time=EVENT_TIME, duration=EVENT_DURATION, color=EVENT_COLOR, type=EVENT_TYPES[0], custom_type=CUSTOM_TYPE):
            url = reverse('event-list')
            return api_client.post(url, {
                        'title': title,
                        'event_time': time,
                        'repeat_duration': duration,
                        'event_color': color,
                        'event_type': type,
                        'custom_event_type': custom_type,
                        'calendar': c_id
                    })
        return _create_event

# class MeetingConf:
#     def create_meeting(api_client:APIClient):
#         def _create_meeting(title=MEETING_TITLE, start=MEETING_START, end=MEETING_END,\
#                           color=MEETING_COLOR, description=MEETING_DESCRIPTION, from_date=MEETING_FROM_DATE, \
#                           until_date=MEETING_UNTIL_DATE, repeat=MEETING_REPEAT):
#             url = reverse('create-meeting')
#             return api_client.post(url, {
#                 'title': title,
#                 'description': description,
#                 'start': start,
#                 'end': end,
#                 'from_date': from_date,
#                 'until_date': until_date,
#                 'repeat': repeat,
#                 'color': color,
#             })
#         return _create_meeting

@pytest.fixture
def create_calendar(api_client:APIClient):
    def _create_calendar(b_id):
        return CalendarConf.create_calendar(api_client)(b_id)
    return _create_calendar

@pytest.fixture
def create_event(api_client:APIClient):
    def _create_event(c_id, title=EVENT_TITLE, time=EVENT_TIME, duration=EVENT_DURATION, color=EVENT_COLOR, type=EVENT_TYPES[0], custom_type=CUSTOM_TYPE):
        return EventConf.create_event(api_client)(c_id, title, time, duration, color, type, custom_type)
    return _create_event

@pytest.fixture
def create_meeting(api_client:APIClient):
    def _create_meeting(c_id, title=MEETING_TITLE, start=MEETING_START, end=MEETING_END,
                   color=MEETING_COLOR, description=MEETING_DESCRIPTION, from_date=MEETING_FROM_DATE,
                   until_date=MEETING_UNTIL_DATE, repeat=MEETING_REPEAT):
        url = reverse('meeting-create-meeting', args=[c_id])
        return api_client.post(url, {
            'title': title,
            'description': description,
            'start': start,
            'end': end,
            'from_date': from_date,
            'until_date': until_date,
            'repeat': repeat,
            'color': color,
        })
    return _create_meeting

@pytest.fixture
def start_meeting(api_client:APIClient):
    def _start_meeting(m_id):
        url = reverse('meeting-start-meeting', args=[m_id])
        return api_client.get(url)
    return _start_meeting