from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from retro.models import RetroSession
from retro.types import RetroSteps
from retro.serializers.sessionserializers import *
from board.models import Board
from accounts.models import Profile



class SessionViewSet(RetrieveModelMixin, CreateModelMixin, 
                     DestroyModelMixin, GenericViewSet):
    queryset = RetroSession.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateSessionSerializer
        if self.request.method == 'GET':
            session_id = self.kwargs.get('pk')
            session = self.queryset.filter(pk=session_id).first()
            serializer_classes = [IceBreakerStepSerializer, ReflectStepSerializer, GroupStepSerializer, VoteStepSerializer]
            if session:
                return serializer_classes[session.retro_step]
            else:
                return CreateSessionSerializer

    def get_serializer_context(self):
        return super().get_serializer_context()

    def create(self, request, *args, **kwargs):
        board = get_object_or_404(Board, pk=request.data.get('board'))
        admin = Profile.objects.filter(pk=request.user.profile).all()
        wowner = Profile.objects.filter(pk=board.workspace.owner).all()
        attendees = board.members.all() | board.admins.all() | wowner | admin
        data = request.data.copy()
        data['attendees'] = attendees
        data['admin'] = request.user.profile
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GetSessionReflect(GenericViewSet):
    queryset = RetroSession.objects.all()
    serializer_class = ReflectStepSerializer
    # permission_classes = [IsAdminUser | IsMeetingBoardMember | IsMeetingBoardAdmin | IsMeetingBoardWorkSpaceOwner]

    @action(detail=True, methods=['get'], url_path='get-session-reflect', url_name='get-session-reflect')
    def get_meeting(self, request, pk):
        sess = self.get_object()
        serializer = self.get_serializer(instance=sess)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetSessionGroup(GenericViewSet):
    queryset = RetroSession.objects.all()
    serializer_class = GroupStepSerializer

    @action(detail=True, methods=['get'], url_path='get-session-group', url_name='get-session-group')
    def get_meeting(self, request, pk):
        sess = self.get_object()
        serializer = self.get_serializer(instance=sess)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetSessionVote(GenericViewSet):
    queryset = RetroSession.objects.all()
    serializer_class = VoteStepSerializer

    @action(detail=True, methods=['get'], url_path='get-session-vote', url_name='get-session-vote')
    def get_meeting(self, request, pk):
        sess = self.get_object()
        serializer = self.get_serializer(instance=sess)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetSessionDiscuss(GenericViewSet):
    queryset = RetroSession.objects.all()
    serializer_class = DiscussStepSerializer

    @action(detail=True, methods=['get'], url_path='get-session-discuss', url_name='get-session-discuss')
    def get_meeting(self, request, pk):
        sess = self.get_object()
        serializer = self.get_serializer(instance=sess)
        return Response(serializer.data, status=status.HTTP_200_OK)