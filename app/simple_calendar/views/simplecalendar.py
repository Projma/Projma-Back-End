from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from ..models import SimpleCalendar
from ..serializers.simplecalendarserializers import  SimpleCalendarSerializer


class SimpleCalendarViewSet(mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    queryset = SimpleCalendar.objects.all()
    serializer_class = SimpleCalendarSerializer