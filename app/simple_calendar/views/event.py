from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from ..models import Event, SimpleCalendar
from ..serializers.eventserializers import EventSerializer
from ..permissions.eventpermissions import *


class EventViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser | IsEventBoardAdmin | IsEventBoardMember | IsEventBoardWorkSpaceOwner]

    def create(self, request, *args, **kwargs):
        try:
            calendar_id = request.data.get('calendar')
            calendar = get_object_or_404(SimpleCalendar, pk=calendar_id)
            # return super().create(request, *args, **kwargs)
            if calendar and request.user.profile in (calendar.board.admins.all() | calendar.board.members.all()) \
                    or request.user.profile == calendar.board.workspace.owner or request.user.is_superuser:
                return super().create(request, *args, **kwargs)
            return Response("Only admins and members of board can create event for this board", status=status.HTTP_403_FORBIDDEN)
        except ValidationError as e:
            if e.message in Event.Error_Messages:
                return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
            raise e

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            if e.message in Event.Error_Messages:
                return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
            raise e
