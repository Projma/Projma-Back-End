from datetime import timedelta, datetime, timezone
from django.db.models import QuerySet
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import mixins
from ..models import SimpleCalendar, Event
from ..serializers.simplecalendarserializers import  SimpleCalendarSerializer
from ..serializers.eventserializers import EventSerializer


class SimpleCalendarViewSet(mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    queryset = SimpleCalendar.objects.all()
    serializer_class = SimpleCalendarSerializer

    @action(detail=True, methods=['get'], url_path='events', serializer_class=EventSerializer)
    def get_period_events(self, request, pk):
        def get_event_occurrences(start, end, event: Event, calendar) -> QuerySet:
            import math
            event_repetition = event.repeat_duration
            event_time = event.event_time.astimezone(timezone.utc)
            start = start.astimezone(timezone.utc)
            end = end.astimezone(timezone.utc)
            query = []
            if event_repetition == 0:
                if start <= event_time <= end:
                    query.append(event)
                return query
            i = math.ceil(((event_time - start).total_seconds() / 86400) / event_repetition) if event_time < start else 0
            j = math.floor(((end - event_time).total_seconds() / 86400) / event_repetition) if end > event_time else -1
            while i <= j:
                event_cpy = model_to_dict(event)
                event_cpy['calendar'] = calendar
                event_cpy = Event(**event_cpy)
                event_cpy.event_time += timedelta(days=i*event_repetition)
                query.append(event_cpy)
                i += 1
            return query
        try:
            start = datetime.strptime(request.GET.get('start'), "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(request.GET.get('end'), "%Y-%m-%d %H:%M:%S")
        except TypeError as e:
            return Response(e.args + ('you may miss the start and end params in query',), status=status.HTTP_400_BAD_REQUEST)
        calendar = self.get_object()
        queryset = []
        for event in list(calendar.events.all()):
            queryset += get_event_occurrences(start, end, event, calendar)
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)