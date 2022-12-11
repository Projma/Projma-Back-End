from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import BoardTemplate, TaskList, Label
from ..serializers.boardtemplateserializer import *

class TemplateViewSet(viewsets.GenericViewSet):
    queryset = BoardTemplate.objects.all()
    serializer_class = BoardTemplateSerializer

    def create_template(self, template_params, tasklists_params, labels_params):
        '''
        template_params = {name:..., description:...}
        tasklists_params = [{title:...}, ...]
        labels_params = [{title:..., color:...}, ...]
        '''
        template_name = template_params['name']
        template_description = template_params['description']
        board_template = BoardTemplate.objects.create(name=template_name, description=template_description)
        tasklists = []
        labels = []
        for tasklist_param in tasklists_params:
            tasklist_title = tasklist_param['title']
            tasklists.append(TaskList.objects.create(title=tasklist_title, board_template=board_template))

        for label_param in labels_params:
            label_title = label_param['title']
            label_color = label_param['color']
            labels.append(Label.objects.create(title=label_title, color=label_color, board_template=board_template))

    @action(detail=False, methods=['get'], url_path='create-project-management-template')
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

    @action(detail=False, methods=['get'], url_path='create-kanban-template')
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

    @action(detail=False, methods=['get'], url_path='project-management')
    def project_management(self, request):
        template = get_object_or_404(BoardTemplate, name='Project Management')
        serializer = self.get_serializer(template)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='kanban')
    def kanban(self, request):
        template = get_object_or_404(BoardTemplate, name='Kanban')
        serializer = self.get_serializer(template)
        return Response(serializer.data, status=status.HTTP_200_OK)