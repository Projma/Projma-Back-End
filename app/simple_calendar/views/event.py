from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from ..models import Event
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
            return super().create(request, *args, **kwargs)
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