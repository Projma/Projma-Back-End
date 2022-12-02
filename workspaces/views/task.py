from django.shortcuts import get_object_or_404 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from ..models import *
from ..serializers.taskserializers import *
from ..permissions.taskpermissions import *
from ..permissions.tasklistpermissions import *
from accounts.serializers import *



class CreateTaskViewSet(viewsets.GenericViewSet):
    queryset = TaskList.objects.all()
    serializer_class = CreateTaskSerializer
    permission_classes = [IsAdminUser | IsTaskListBoardMember | IsTaskListBoardAdmin | IsTaskListBoardWorkSpaceOwner]
    @action(detail=True, methods=['post'])
    def create_task(self, request, pk):
        tl = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(tasklist=tl)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateTaskViewSet(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = UpdateTaskSerializer
    permission_classes = [IsAdminUser | IsTaskBoardMember | IsTaskBoardAdmin | IsTaskBoardWorkSpaceOwner]
    @action(detail=True, methods=['patch'])
    def update_task(self, request, pk):
        task = self.get_object()
        serializer = self.get_serializer(instance=task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)