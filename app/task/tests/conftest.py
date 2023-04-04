import pytest
from datetime import date, timedelta
from rest_framework.test import APIClient
from board.tests.conftest import *

START_DATE = date.today()
END_DATE = START_DATE + timedelta(10)
TITLE = "test_task1"

class TaskConf:
    def create_task(api_client:APIClient):
        def _create_task(tl_id, name=TITLE, start_date=START_DATE, end_date=END_DATE):
            return api_client.post(f'/task/{tl_id}/create-task/', {'title': name, 'start_date': start_date, 'end_date': end_date})
        return _create_task


@pytest.fixture
def create_task(api_client:APIClient):
    '''you should create a board then tasklist at first. it returns response(task object)'''
    def _create_task(tl_id, name=TITLE, start_date=START_DATE, end_date=END_DATE):
        return TaskConf.create_task(api_client)(tl_id, name, start_date, end_date)
    return _create_task