from django.shortcuts import get_object_or_404 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from ..models import *
from ..serializers.tasklistserializers import *
from ..permissions.tasklistpermissions import *
from accounts.serializers import *


class CreateTaskListViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsBoardMember | IsAdminUser | IsBoardAdmin | IsBoardWorkSpaceOwner]
    @action(detail=True, methods=['post'])
    def create_tasklist(self, request, pk):
        board = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(board=board)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateTaskListViewSet(viewsets.GenericViewSet):
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAdminUser | IsTaskListBoardMember | IsTaskListBoardAdmin | IsTaskListBoardWorkSpaceOwner]
    @action(detail=True, methods=['patch'])
    def update_tasklist(self, request, pk):
        tl = self.get_object()
        serializer = self.get_serializer(instance=tl, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteTaskListViewSet(viewsets.GenericViewSet):
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAdminUser | IsTaskListBoardMember | IsTaskListBoardAdmin | IsTaskListBoardWorkSpaceOwner]
    @action(detail=True, methods=['delete'])
    def delete_tasklist(self, request, pk):
        tl = self.get_object()
        tl.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReorderTaskListsViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = ReorderTaskListSerializer
    permission_classes = [IsBoardMember | IsAdminUser | IsBoardAdmin | IsBoardWorkSpaceOwner]
    @action(detail=True, methods=['put'])
    def reorder_tasklists(self, request, pk):
        board = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            board.reorder_tasklists(serializer.data['order'])
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(TaskListSerializer(instance=board.tasklists.all(), many=True).data, status=status.HTTP_200_OK)

