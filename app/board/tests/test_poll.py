from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from board.models import Poll, PollAnswer
import pytest


@pytest.mark.django_db
class TestCreatePoll:
    def create_poll(create_board, create_poll, is_multianswer=False, is_known=True):
        '''return a response with a poll object'''
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED

        board_id = response.data['id']
        response = create_poll(board_id, is_multianswer=is_multianswer, is_known=is_known)
        return response

    def test_create_valid_poll_returns_201(self, create_board, create_poll):
        response = TestCreatePoll.create_poll(create_board, create_poll)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_invalid_poll_returns_400(self, create_board, create_poll):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED

        board_id = response.data['id']
        response = create_poll(board_id, question='')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeletePoll:
    def test_delete_exist_poll_returns_204(self, create_board, create_poll, api_client):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED

        board_id = response.data['id']
        response = create_poll(board_id)
        assert response.status_code == status.HTTP_201_CREATED

        poll_id = response.data['id']
        url = reverse('poll-detail', args=[poll_id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_invalid_poll_returns_400(self, create_board, create_poll, api_client):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED

        board_id = response.data['id']
        response = create_poll(board_id)
        assert response.status_code == status.HTTP_201_CREATED

        poll_id = response.data['id']
        url = reverse('poll-detail', args=[poll_id+1])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateAnswer:
    def test_create_valid_answer_returns_201(self, create_board, create_poll, create_answer):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED

        board_id = response.data['id']
        response = create_poll(board_id)
        assert response.status_code == status.HTTP_201_CREATED

        poll_id = response.data['id']
        response = create_answer(poll_id)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_invalid_answer_returns_400(self, create_board, create_poll, create_answer):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED

        board_id = response.data['id']
        response = create_poll(board_id)
        assert response.status_code == status.HTTP_201_CREATED

        poll_id = response.data['id']
        response = create_answer(poll_id, text='')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteAnswer:
    def test_delete_exist_answer_returns_204(self, create_board, create_poll, create_answer, api_client):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED

        board_id = response.data['id']
        response = create_poll(board_id)
        assert response.status_code == status.HTTP_201_CREATED

        poll_id = response.data['id']
        response = create_answer(poll_id)
        assert response.status_code == status.HTTP_201_CREATED

        answer_id = response.data['id']
        url = reverse('poll-answers-detail', args=[answer_id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_invalid_answer_returns_204(self, create_board, create_poll, create_answer, api_client):
        response = create_board()
        assert response.status_code == status.HTTP_201_CREATED

        board_id = response.data['id']
        response = create_poll(board_id)
        assert response.status_code == status.HTTP_201_CREATED

        poll_id = response.data['id']
        response = create_answer(poll_id)
        assert response.status_code == status.HTTP_201_CREATED

        answer_id = response.data['id']
        url = reverse('poll-answers-detail', args=[answer_id+1])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestVote:
    def test_vote_once_returns_200(self, create_board, create_poll, create_answer, api_client):
        response = TestCreatePoll.create_poll(create_board, create_poll)
        poll_id = response.data['id']
        response = create_answer(poll_id, text='ans1', order=1)
        ans1 = response.data
        assert response.status_code == status.HTTP_201_CREATED
        assert PollAnswer.objects.get(pk=ans1['id']).count == 0
        
        url = reverse('poll-answers-detail', args=[ans1['id']]) + 'vote/'
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert PollAnswer.objects.get(pk=ans1['id']).count == 1
        
        response = create_answer(poll_id, text='ans2', order=2)
        ans2 = response.data
        assert response.status_code == status.HTTP_201_CREATED
        assert PollAnswer.objects.get(pk=ans2['id']).count == 0 and PollAnswer.objects.get(pk=ans1['id']).count == 1
        
        url = reverse('poll-answers-detail', args=[ans2['id']]) + 'vote/'
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert PollAnswer.objects.get(pk=ans2['id']).count == 1 and PollAnswer.objects.get(pk=ans1['id']).count == 1

    def test_vote_more_than_once_returns_400(self, create_board, create_poll, create_answer, api_client):
        response = TestCreatePoll.create_poll(create_board, create_poll)
        poll_id = response.data['id']
        response = create_answer(poll_id, text='ans1', order=1)
        ans1 = response.data
        assert response.status_code == status.HTTP_201_CREATED
        assert PollAnswer.objects.get(pk=ans1['id']).count == 0
        
        url = reverse('poll-answers-detail', args=[ans1['id']]) + 'vote/'
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert PollAnswer.objects.get(pk=ans1['id']).count == 1
        
        response = api_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert PollAnswer.objects.get(pk=ans1['id']).count == 1

    def test_vote_closed_poll_returns_400(self, create_board, create_poll, create_answer, api_client):
        response = TestCreatePoll.create_poll(create_board, create_poll)
        poll_id = response.data['id']
        response = create_answer(poll_id, text='ans1', order=1)
        ans1 = response.data
        assert response.status_code == status.HTTP_201_CREATED
        assert PollAnswer.objects.get(pk=ans1['id']).count == 0
        poll = Poll.objects.get(pk=poll_id)
        poll.is_open = False
        poll.save()
        assert Poll.objects.get(pk=poll_id).is_open == False
        
        url = reverse('poll-answers-detail', args=[ans1['id']]) + 'vote/'
        response = api_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert PollAnswer.objects.get(pk=ans1['id']).count == 0


@pytest.mark.django_db
class TestRetractVotes:
    def test_retract_votes_returns_204(self, create_board, create_poll, create_answer, api_client):
        response = TestCreatePoll.create_poll(create_board, create_poll)
        poll_id = response.data['id']
        response = create_answer(poll_id, text='ans1', order=1)
        ans1 = response.data
        assert response.status_code == status.HTTP_201_CREATED
        assert PollAnswer.objects.get(pk=ans1['id']).count == 0
        
        url = reverse('poll-answers-detail', args=[ans1['id']]) + 'vote/'
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert PollAnswer.objects.get(pk=ans1['id']).count == 1
        
        response = create_answer(poll_id, text='ans2', order=2)
        ans2 = response.data
        assert response.status_code == status.HTTP_201_CREATED
        assert PollAnswer.objects.get(pk=ans2['id']).count == 0 and PollAnswer.objects.get(pk=ans1['id']).count == 1
        
        url = reverse('poll-answers-detail', args=[ans2['id']]) + 'vote/'
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert PollAnswer.objects.get(pk=ans2['id']).count == 1 and PollAnswer.objects.get(pk=ans1['id']).count == 1
        
        url = reverse('poll-answers-detail', args=[ans1['id']]) + 'retract-vote/'
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert PollAnswer.objects.get(pk=ans1['id']).count == 0
        url = reverse('poll-answers-detail', args=[ans2['id']]) + 'retract-vote/'
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert PollAnswer.objects.get(pk=ans2['id']).count == 0

    def test_retract_votes_from_closed_poll_returns_400(self, create_board, create_poll, create_answer, api_client):
        response = TestCreatePoll.create_poll(create_board, create_poll)
        poll_id = response.data['id']
        response = create_answer(poll_id, text='ans1', order=1)
        ans1 = response.data
        assert response.status_code == status.HTTP_201_CREATED
        assert PollAnswer.objects.get(pk=ans1['id']).count == 0
        
        url = reverse('poll-answers-detail', args=[ans1['id']]) + 'vote/'
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert PollAnswer.objects.get(pk=ans1['id']).count == 1
        
        poll = Poll.objects.get(pk=poll_id)
        poll.is_open = False
        poll.save()
        assert Poll.objects.get(pk=poll_id).is_open == False
        
        url = reverse('poll-answers-detail', args=[ans1['id']]) + 'retract-vote/'
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert PollAnswer.objects.get(pk=ans1['id']).count == 1