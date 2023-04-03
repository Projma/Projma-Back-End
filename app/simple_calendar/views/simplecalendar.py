from datetime import timedelta, datetime, timezone
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAdminUser
from task.models import Task
from ..models import SimpleCalendar, Event
from ..serializers.simplecalendarserializers import  SimpleCalendarSerializer
from ..serializers.eventserializers import EventSerializer
from ..permissions.calendarpermissions import *


class SimpleCalendarViewSet(mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    queryset = SimpleCalendar.objects.all()
    serializer_class = SimpleCalendarSerializer
    permission_classes = [IsAdminUser | IsCalendarBoardMember | IsCalendarBoardAdmin | IsCalendarBoardWorkSpaceOwner]

    @action(detail=True, methods=['get'], url_path='events', url_name='events', serializer_class=EventSerializer)
    def get_period_events(self, request, pk):
        def get_event_occurrences(start, end, event: Event):
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
            i = math.ceil(((start - event_time).total_seconds() / 86400) / event_repetition) if event_time < start else 0
            j = math.floor(((end - event_time).total_seconds() / 86400) / event_repetition) if end > event_time else -1
            while i <= j:
                event_cpy = model_to_dict(event)
                event_cpy['calendar'] = calendar
                event_cpy = Event(**event_cpy)
                event_cpy.event_time += timedelta(days=i*event_repetition)
                query.append(event_cpy)
                i += 1
            return query
        def convert_date_to_datetime(date):
            return datetime(date.year, date.month, date.day, 23, 59, 59)
        def convert_task_to_event(task: Task):
            event = Event(title=task.title, description=task.description,
                          event_color="#B325be", event_type=Event.EVENT_TYPE_CHOICES[0][1])
            event.event_time = convert_date_to_datetime(task.end_date)
            event.calendar = calendar
            # event.pk = task.pk
            return event
        calendar = self.get_object()
        try:
            start = datetime.strptime(request.GET.get('start'), "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(request.GET.get('end'), "%Y-%m-%d %H:%M:%S")
        except TypeError as e:
            return Response(e.args + ('you may miss the start and end params in query',), status=status.HTTP_400_BAD_REQUEST)
        queryset = []
        for event in list(calendar.events.all()):
            queryset += get_event_occurrences(start, end, event)
        board = calendar.board
        tasklists = board.tasklists.all()
        for tl in tasklists:
            tasks = tl.tasks.all()
            for task in tasks:
                if start <= convert_date_to_datetime(task.end_date) <= end:
                    queryset.append(convert_task_to_event(task))
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
