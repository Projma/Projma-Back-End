from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from task.models import Task
from board.models import Board
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

    @action(detail=False, methods=['get'], url_path='board-members-activity/(?P<b_id>[^/.]+)')
    def board_members_activity(self, request, *args, **kwargs):
        b_id = kwargs.get('b_id')
        if not b_id:
            return Response({'error': 'Board id is required'}, status=status.HTTP_400_BAD_REQUEST)
        b_members = (get_object_or_404(Board, pk=b_id).members.all() | get_object_or_404(Board, pk=b_id).admins.all())
        qs = b_members.values('user__username')\
                    .annotate(estimates=Sum('tasks__estimate'),
                              dons=Sum('tasks__spend'),
                              out_of_estimates=Sum('tasks__out_of_estimate')).all()
        chart = Chart('فعالیت اعضا', 'فرد', 'فعالیت')
        xdata = [m['user__username'] for m in qs.values('user__username')]
        estimates_data = [m['estimates'] for m in qs.values('estimates')]
        dons_data = [m['dons'] for m in qs.values('dons')]
        out_of_estimates_data = [m['out_of_estimates'] for m in qs.values('out_of_estimates')]
        ydata = [{'estimates':estimates_data}, {'dons': dons_data}, {'out_of_estimates': out_of_estimates_data}]
        for x in xdata:
            chart.add_x(x)
        for y in ydata:
            chart.add_y(y)
        return Response(chart.data, status=200)


    @action(detail=False, methods=['get'], url_path='my-assign-tasks-for-all-boards/(?P<user_id>[^/.]+)')
    def my_assign_tasks_for_all_boards(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        if not user_id:
            return Response({'error': 'User id is required'}, status=status.HTTP_400_BAD_REQUEST)
        my_boards = (Board.objects.filter(members__user__id=user_id).values('name').all() | Board.objects.filter(admins__user__id=user_id).values('name').all()).distinct()
        all_board_tasks = {b['name']: Task.objects.filter(tasklist__board__name=b['name']).count() for b in my_boards}
        my_boards = [b['name'] for b in my_boards]
        qs = Task.objects.filter(doers__user__id=user_id)\
            .values('tasklist__board__name')\
            .annotate(count=Count('tasklist__board')).all()
        result = self.merge_querysets(qs.all(), my_boards, 'tasklist__board__name')
        chart = Chart('تعداد فعالیت من برای هر برد', 'برد', 'تعداد')
        for key, value in result.items():
            chart.add_data([key, 'تمام کارهای برد'], [value, all_board_tasks[key]])
        return Response(chart.data, status=status.HTTP_200_OK)