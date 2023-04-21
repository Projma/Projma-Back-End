import requests as request_lib
from django.urls import reverse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from board.serializers.pollserializers import *
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from board.models import Poll, Board
from board.permissions.pollpermissions import *


class PollViewSet(CreateModelMixin, 
                  DestroyModelMixin,
                  RetrieveModelMixin,
                  viewsets.GenericViewSet):

    serializer_class = PollSerializer
    queryset = Poll.objects.all()
    permission_classes = [IsAdminUser | IsPollBoardAdminPermission | IsPollBoardMemberPermission | IsPollBoardWorkSpaceOwnerPermission]

    @action(detail=True, url_path='retract-all-votes', methods=['delete'])
    def retract_all_votes(self, request, pk):
        poll = self.get_object()
        if poll.is_open:
            host = request.get_host()
            scheme = request.scheme + '://'
            user = request.user.profile
            poll_ans = user.votes.filter(poll=poll)
            for ans in poll_ans:
                url = scheme  + host + reverse('poll-answers-detail', args=[ans.pk]) + 'retract-vote/'
                response = request_lib.delete(url, headers=request.headers, params=request.query_params)
                if response.status_code != status.HTTP_204_NO_CONTENT:
                    return response
            return Response("", status=status.HTTP_204_NO_CONTENT)
        return Response("Poll is closed. You can not retract your votes", status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, url_path='show-result', methods=['get'])
    def show_result(self, request, pk):
        poll = self.get_object()
        if poll.is_known:
            serializer = KnownPollSerializer(poll, context={'request': request})
        else:
            serializer = UnknownPollSerializer(poll, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, url_path='close', methods=['patch'])
    def close_poll(self, request, pk):
        poll = self.get_object()
        if poll.is_open:
            poll.is_open = False
            poll.save()
            return Response("Ok", status=status.HTTP_200_OK)
        return Response("Poll is already closed.", status=status.HTTP_400_BAD_REQUEST)


class PollAnswerViewSet(CreateModelMixin,
                        DestroyModelMixin,
                        viewsets.GenericViewSet):

    serializer_class = PollAnswerSerializer
    queryset = PollAnswer.objects.all()
    permission_classes = [IsAdminUser | IsPollAnswerBoardAdminPermission | IsPollAnswerBoardMemberPermission | IsPollAnswerWorkSpaceOwnerPermission]

    @action(detail=True, url_path='vote', methods=['post'])
    def vote(self, request, pk):
        poll_ans = self.get_object()
        if poll_ans.poll.is_open:
            user = request.user.profile
            if poll_ans.voters.filter(user=user.pk).count() > 0:
                return Response("You can not vote for a single option more than once.", status=status.HTTP_400_BAD_REQUEST)
            poll_ans.voters.add(user)
            poll_ans.count += 1
            poll_ans.save()
            return Response("Ok", status=status.HTTP_200_OK)
        return Response("Poll is closed. You can not vote", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, url_path='retract-vote', methods=['delete'])
    def retract_vote(self, request, pk):
        poll_ans = self.get_object()
        if poll_ans.poll.is_open:
            user = request.user.profile
            if poll_ans.voters.filter(user=user.pk).count() < 1:
                return Response("You have not voted to this option", status=status.HTTP_400_BAD_REQUEST)
            poll_ans.voters.remove(user)
            poll_ans.count -= 1
            poll_ans.save()
            return Response("", status=status.HTTP_204_NO_CONTENT)
        return Response("Poll is closed. You can not retract your vote", status=status.HTTP_400_BAD_REQUEST)