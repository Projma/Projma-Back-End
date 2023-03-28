from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import TaskList, Label, WorkSpace
from board.models import Board
from ..serializers.boardtemplateserializer import *
from board.serializers.boardserializers import BoardOverviewSerializer, BoardAdminSerializer
from ..serializers.tasklistserializers import TaskListSerializer
from ..serializers.labelserializers import LabelSerializer


def create_template(template_params, tasklists_params, labels_params):
    '''
    template_params = {name:..., description:..., background_pic:...}
    tasklists_params = [{title:...}, ...]
    labels_params = [{title:..., color:...}, ...]
    '''
    template_name = template_params.get('name')
    template_description = template_params.get('description')
    template_background_pic = template_params.get('background_pic')
    board_template = Board.objects.create(name=template_name, description=template_description, background_pic=template_background_pic, is_template=True)
    tasklists = []
    labels = []
    for tasklist_param in tasklists_params:
        tasklist_title = tasklist_param.get('title')
        tasklists.append(TaskList.objects.create(title=tasklist_title, board=board_template))

    for label_param in labels_params:
        label_title = label_param.get('title')
        label_color = label_param.get('color')
        labels.append(Label.objects.create(title=label_title, color=label_color, board=board_template))


class TemplateViewSet(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = BoardTemplateSerializer

    def get_queryset(self):
        return Board.objects.filter(is_template=True)


class CreateBoardFromTemplateViewSet(viewsets.GenericViewSet):
    serializer_class = BoardOverviewSerializer

    @action(detail=True, methods=['get'], url_path='create-board-from-template/(?P<w_id>[^/.]+)')
    def create_board_from_template(self, request, pk, w_id):
        template = get_object_or_404(Board, pk=pk)
        workspace = get_object_or_404(WorkSpace, pk=w_id)
        if workspace.owner != request.user.profile:
            return Response("Only owner of workspace can create board", status=status.HTTP_403_FORBIDDEN)
        tasklists = template.tasklists.all()
        labels = template.labels.all()
        template_dict = template.__dict__
        if template_dict['background_pic'] == '':
            template_dict['background_pic'] = None
        b_pic = template_dict['background_pic']
        template_dict['background_pic'] = None
        serializer = BoardAdminSerializer(data=template_dict)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_template=False, workspace=workspace)
        board = get_object_or_404(Board, pk=serializer.data['id'])
        board.background_pic = b_pic
        board.save()
        for tl in tasklists:
            tasklist_dict = get_object_or_404(TaskList, pk=tl.id).__dict__
            tasklist_serializer = TaskListSerializer(data=tasklist_dict)
            tasklist_serializer.is_valid(raise_exception=True)
            tasklist_serializer.save(board=board)
        for l in labels:
            label_dict = get_object_or_404(Label, pk=l.id).__dict__
            label_serializer = LabelSerializer(data=label_dict)
            label_serializer.is_valid(raise_exception=True)
            label_serializer.save(board=board)
        serializer = BoardOverviewSerializer(board)
        return Response(serializer.data, status=status.HTTP_201_CREATED)