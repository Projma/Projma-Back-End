from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from ..models import Task, TaskList, Board
from ..chart_model import Chart

class ChartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def merge_querysets(self, qs1, qs2, qskey, qsvalue='count'):
        temp_set = set()
        for item in qs1:
            temp_set.add(item[qskey])
        temp_set.update(qs2)
        result = {item: 0 for item in temp_set}
        for item in qs1:
            result[item[qskey]] = item[qsvalue]
        return result

    @action(detail=False, methods=['get'], url_path='board-members-assign-tasks/(?P<b_id>[^/.]+)')
    def board_members_assign_tasks(self, request, *args, **kwargs):
        b_id = kwargs.get('b_id')
        if not b_id:
            return Response({'error': 'Board id is required'}, status=status.HTTP_400_BAD_REQUEST)
        b_members = (get_object_or_404(Board, pk=b_id).members.all() | get_object_or_404(Board, pk=b_id).admins.all()).values('user__username').all().distinct()
        b_members = [m['user__username'] for m in b_members]
        qs = Task.objects.filter(tasklist__board__id=b_id)\
            .values('doers__user__username')\
            .annotate(count=Count('doers')).all()
        result = self.merge_querysets(qs.all(), b_members, 'doers__user__username')
        chart = Chart('تعداد کار واگذار شده به هر فرد', 'فرد', 'تعداد')
        for key, value in result.items():
            chart.add_data([key], [value])
        return Response(chart.data, status=status.HTTP_200_OK)
