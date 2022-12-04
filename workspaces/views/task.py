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


class AddLabelsToTask(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = UpdateTaskLabelsSerializer
    permission_classes = [IsAdminUser | IsTaskBoardMember | IsTaskBoardAdmin | IsTaskBoardWorkSpaceOwner]
    @action(detail=True, methods=['patch'])
    def add_labels_to_task(self, request, pk):
        task = self.get_object()
        data = request.data
        try:
            for prelabel in task.labels.all():
                if prelabel.id not in data['labels']:
                    data['labels'].append(prelabel.id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance=task, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DeleteLabelsFromTask(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = UpdateTaskLabelsSerializer
    permission_classes = [IsAdminUser | IsTaskBoardMember | IsTaskBoardAdmin | IsTaskBoardWorkSpaceOwner]
    @action(detail=True, methods=['patch'])
    def delete_labels_from_task(self, request, pk):
        task = self.get_object()
        data = {'labels': [prelabel.id for prelabel in task.labels.all()]}
        try:
            for lid in request.data['labels']:
                if lid in data['labels']:
                    data['labels'].remove(lid)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance=task, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AddDoersToTask(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = UpdateTaskDoersSerializer
    permission_classes = [IsAdminUser | IsTaskBoardMember | IsTaskBoardAdmin | IsTaskBoardWorkSpaceOwner]
    @action(detail=True, methods=['patch'])
    def add_doers_to_task(self, request, pk):
        task = self.get_object()
        data = request.data
        try:
            for predoer in task.doers.all():
                if predoer.pk not in data['doers']:
                    data['doers'].append(predoer.pk)
                print(data['doers'])
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance=task, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteDoersFromTasl(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = UpdateTaskDoersSerializer
    permission_classes = [IsAdminUser | IsTaskBoardMember | IsTaskBoardAdmin | IsTaskBoardWorkSpaceOwner]
    @action(detail=True, methods=['patch'])
    def delete_doers_from_task(self, request, pk):
        task = self.get_object()
        data = {'doers': [predoer.pk for predoer in task.doers.all()]}
        try:
            for did in request.data['doers']:
                if did in data['doers']:
                    data['doers'].remove(did)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance=task, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GetTaskPreview(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskPreviewSerializer
    permission_classes = [IsAdminUser | IsTaskBoardMember | IsTaskBoardAdmin | IsTaskBoardWorkSpaceOwner]
    @action(detail=True, methods=['get'])
    def preview(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)