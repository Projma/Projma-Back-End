from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from ..models import Event
from ..serializers.eventserializers import EventSerializer


class EventViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer