from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from ..models import CheckList
from ..serializers.checklistserializers import *
from ..permissions.checklistpermissions import *
# from ..permissions.taskpermissions import *
from task.permissions.taskpermissions import *
from task.models import Task


class CreateOrReadCheckListViewSet(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = CreateOrReadCheckListSerializer
    permission_classes = [IsAdminUser | IsTaskBoardMember | IsTaskBoardAdmin | IsTaskBoardWorkSpaceOwner]

    @action(detail=True, methods=['post'], url_path='create-checklist')
    def create_checklist(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(task=task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='get-all-checklists')
    def get_all_checklists(self, request, *args, **kwargs):
        task = self.get_object()
        queryset = CheckList.objects.filter(task=task).all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateCheckListViewSet(UpdateModelMixin, viewsets.GenericViewSet):
    queryset = CheckList.objects.all()
    serializer_class = UpdateCheckListSerializer
    permission_classes = [IsCheckListBoardMember | IsCheckListBoardAdmin | IsCheckListBoardWorkSpaceOwner | IsAdminUser]


class DeleteCheckListViewSet(DestroyModelMixin, viewsets.GenericViewSet):
    queryset = CheckList.objects.all()
    serializer_class = CreateOrReadCheckListSerializer
    permission_classes = [IsCheckListBoardMember | IsCheckListBoardAdmin | IsCheckListBoardWorkSpaceOwner | IsAdminUser]