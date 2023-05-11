from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from retro.models import RetroSession
from retro.serializers.sessionserializers import *
from board.models import Board
from accounts.models import Profile



class SessionViewSet(RetrieveModelMixin, CreateModelMixin, 
                     DestroyModelMixin, GenericViewSet):
    queryset = RetroSession.objects.all()
    serializer_class = CreateSessionSerializer

    def create(self, request, *args, **kwargs):
        board = get_object_or_404(Board, pk=request.data.get('board'))
        wowner = Profile.objects.filter(pk=board.workspace.owner).all()
        attendees = board.members.all() | board.admins.all() | wowner
        data = request.data.copy()
        data['attendees'] = attendees
        data['admin'] = request.user.profile
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)