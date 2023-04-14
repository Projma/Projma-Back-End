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
                  RetrieveModelMixin,
                  viewsets.GenericViewSet):

    serializer_class = PollSerializer
    queryset = Poll.objects.all()