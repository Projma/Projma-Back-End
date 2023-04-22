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
        estimates_data = [item['estimates'] if item['estimates'] else 0 for item in qs.values('estimates')]
        dons_data = [item['dons'] if item['dons'] else 0 for item in qs.values('dons')]
        out_of_estimates_data = [item['out_of_estimates'] if item['out_of_estimates'] else 0 for item in qs.values('out_of_estimates')]
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

    @action(detail=True, methods=['get'], url_path='board-label-activity')
    def board_label_activity(self, request, *args, **kwargs):
        board = self.get_object()
        alltasks = []
        for tl in board.tasklists.all():
            alltasks += tl.tasks.all()
        chart = Chart('میزان فعالیت برحسب برچسب', 'برچسب', 'ساعت')
        labels = list(board.labels.all())
        print(labels)
        for lb in labels:
            chart.add_x(lb.title)
            sum = 0
            for t in alltasks:
                if lb in t.labels.all():
                    sum += t.spend
            chart.add_y(sum)
        print(chart.xdata)
        print(chart.ydata)
        return Response(chart.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='board-progress')
    def board_progress(self, request, pk):
        board = self.get_object()
        chart = Chart('میزان پیشروی', 'لیست', 'وضعیت')
        est_data = []
        sp_data = []
        for tl in board.tasklists.all():
            chart.add_x(tl.title)
            est = 0
            spend = 0
            for t in tl.tasks.all():
                est += t.estimate
                spend += t.spend
            est_data.append(est)
            sp_data.append(spend)
        chart.ydata = [{'estimate': est_data, 'spend':sp_data}]
        return Response(chart.data, status=status.HTTP_200_OK)