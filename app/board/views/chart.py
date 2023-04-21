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

class ChartViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Board.objects.all()

    def get_estimate_and_done_and_out(self, qs):
        estimates_data = [item['estimates'] for item in qs.values('estimates')]
        dons_data = [item['dons'] for item in qs.values('dons')]
        out_of_estimates_data = [item['out_of_estimates'] for item in qs.values('out_of_estimates')]
        ydata = [{'estimates':estimates_data}, {'dons': dons_data}, {'out_of_estimates': out_of_estimates_data}]
        return ydata

    @action(detail=True, methods=['get'], url_path='board-members-activity')
    def board_members_status(self, request, *args, **kwargs):
        b_id = self.get_object().pk
        if not b_id:
            return Response({'error': 'Board id is required'}, status=status.HTTP_400_BAD_REQUEST)
        b_members = (get_object_or_404(Board, pk=b_id).members.all() | get_object_or_404(Board, pk=b_id).admins.all())
        qs = b_members.values('user__username')\
                    .annotate(estimates=Sum('tasks__estimate'),
                              dons=Sum('tasks__spend'),
                              out_of_estimates=Sum('tasks__out_of_estimate')).all()
        chart = Chart('فعالیت اعضا', 'اعضا', 'فعالیت')
        xdata = [m['user__username'] for m in qs.values('user__username')]
        ydata = self.get_estimate_and_done_and_out(qs)
        for x in xdata:
            chart.add_x(x)
        for y in ydata:
            chart.add_y(y)
        return Response(chart.data, status=200)


    @action(detail=True, methods=['get'], url_path='board-tasklists-activity')
    def board_tasklists_status(self, request, *args, **kwargs):
        b_id = self.get_object().pk
        if not b_id:
            return Response({'error': 'Board id is required'}, status=status.HTTP_400_BAD_REQUEST)
        b_tasklists = get_object_or_404(Board, pk=b_id).tasklists.all()
        qs = b_tasklists.values('title')\
                    .annotate(estimates=Sum('tasks__estimate'),
                              dons=Sum('tasks__spend'),
                              out_of_estimates=Sum('tasks__out_of_estimate')).all()
        chart = Chart('نتایج فعالیت ها', 'لیست فعالیت ها', 'فعالیت')
        xdata = [tl['title'] for tl in qs.values('title')]
        ydata = self.get_estimate_and_done_and_out(qs)
        for x in xdata:
            chart.add_x(x)
        for y in ydata:
            chart.add_y(y)
        return Response(chart.data, status=200)