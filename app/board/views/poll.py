from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from board.serializers.pollserializers import *
from rest_framework.decorators import action
from board.models import Poll, Board


class PollViewSet(CreateModelMixin, 
                  DestroyModelMixin, 
                  viewsets.GenericViewSet):

    serializer_class = PollSerializer
    queryset = Poll.objects.all()


class PollAnswerViewSet(CreateModelMixin,
                        DestroyModelMixin,
                        viewsets.GenericViewSet):

    serializer_class = PollAnswerSerializer
    queryset = PollAnswer.objects.all()

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