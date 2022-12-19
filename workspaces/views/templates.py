from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Board, TaskList, Label
from ..serializers.boardtemplateserializer import *


class TemplateViewSet(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = BoardTemplateSerializer

    def get_queryset(self):
        return Board.objects.filter(is_template=True)

    def create_template(self, template_params, tasklists_params, labels_params):
        '''
        template_params = {name:..., description:...}
        tasklists_params = [{title:...}, ...]
        labels_params = [{title:..., color:...}, ...]
        '''
        template_name = template_params.get('name')
        template_description = template_params.get('description')
        board_template = Board.objects.create(name=template_name, description=template_description, is_template=True)
        tasklists = []
        labels = []
        for tasklist_param in tasklists_params:
            tasklist_title = tasklist_param.get('title')
            tasklists.append(TaskList.objects.create(title=tasklist_title, board=board_template))

        for label_param in labels_params:
            label_title = label_param.get('title')
            label_color = label_param.get('color')
            labels.append(Label.objects.create(title=label_title, color=label_color, board=board_template))

    @action(detail=False, methods=['post'], url_path='create-project-management-template')
    def create_project_management_template(self, request):
        template_params = {'name': 'Project Management', 'description': 'Project Management Template'}
        tasklists_params = [{'title': 'Project Resources'}, \
                {'title': 'Questions For Next Meeting'}, \
                {'title': 'Project Progress'}, \
                {'title': 'To Do'}, \
                {'title': 'Pending'}, \
                {'title': 'Blocked'}, \
                {'title': 'Done'}]
        labels_params = [{'title': 'Copy Request', 'color': '#D6FF3680'}, \
                {'title': 'Priority', 'color': '#FF805980'}, \
                {'title': 'Design Team', 'color': '#C712BA87'}]
        self.create_template(template_params, tasklists_params, labels_params)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='create-kanban-template')
    def create_kanban_template(self, request):
        template_params = {'name': 'Kanban', 'description': 'Kanban Template'}
        tasklists_params = [{'title': 'Backlog'}, \
                {'title': 'Design'}, \
                {'title': 'To Do'}, \
                {'title': 'Doing'}, \
                {'title': 'Code Review'}, \
                {'title': 'Testing'},
                {'title': 'Done'}]
        labels_params = [{'title': 'In Queue', 'color': '#FF78FA96'}, \
                {'title': 'In Progress', 'color': '#FFCD2696'}, \
                {'title': 'Completed', 'color': '#66FF0F96'}]
        self.create_template(template_params, tasklists_params, labels_params)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='create-agile-board-template')
    def create_agile_board_template(self, request):
        template_params = {'name': 'Agile Board', 'description': 'Agile Board Template'}
        tasklists_params = [{'title': 'Done'}, \
                {'title': 'Current Sprint'}, \
                {'title': 'In Progress'}, \
                {'title': 'On Hold'}, \
                {'title': 'Next Up'}, \
                {'title': 'Questions'}]
        labels_params = [{'title': 'Demand Marketing', 'color': '#E221FF96'}, \
                {'title': 'Planning', 'color': '#5EFF0F96'}, \
                {'title': 'Happiness', 'color': '#FF5CE396'}, \
                {'title': 'Government', 'color': '#14CFFF96'},\
                {'title': 'Partners', 'color': '#1C94FF96'}]
        self.create_template(template_params, tasklists_params, labels_params)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='create-simple-template')
    def create_simple_template(self, request):
        template_params = {'name': 'Simple Template', 'description': 'Simple Board Template'}
        tasklists_params = [{'title': 'Brainstorm'}, \
                {'title': 'To Do'}, \
                {'title': 'Doing'},\
                {'title': 'Done'}]
        labels_params = []
        self.create_template(template_params, tasklists_params, labels_params)
        return Response(status=status.HTTP_201_CREATED)
