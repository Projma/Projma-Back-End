from django.shortcuts import get_object_or_404 
from rest_framework import viewsets
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from ..models import *
from ..serializers.taskserializers import *
from ..serializers.attachmentserializer import *
from ..serializers.labelserializers import *
from ..permissions.taskpermissions import *
from ..permissions.tasklistpermissions import *
from accounts.serializers import *
from ..permissions.attachmentpermissions import *



class CreateTaskViewSet(viewsets.GenericViewSet):
    queryset = TaskList.objects.all()
    serializer_class = CreateTaskSerializer
    permission_classes = [IsAdminUser | IsTaskListBoardMember | IsTaskListBoardAdmin | IsTaskListBoardWorkSpaceOwner]
    @action(detail=True, methods=['post'], url_path='create-task')
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
    @action(detail=True, methods=['patch'], url_path='update-task')
    def update_task(self, request, pk):
        task = self.get_object()
        serializer = self.get_serializer(instance=task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteTaskViewSet(DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskOverviewSerializer
    permission_classes = [IsAdminUser | IsTaskBoardAdmin | IsTaskBoardMember | IsTaskBoardWorkSpaceOwner]


class AddLabelsToTaskViewSet(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = UpdateTaskLabelsSerializer
    permission_classes = [IsAdminUser | IsTaskBoardMember | IsTaskBoardAdmin | IsTaskBoardWorkSpaceOwner]
    @action(detail=True, methods=['patch'], url_path='add-labels-to-task')
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


class DeleteLabelsFromTaskViewSet(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = UpdateTaskLabelsSerializer
    permission_classes = [IsAdminUser | IsTaskBoardMember | IsTaskBoardAdmin | IsTaskBoardWorkSpaceOwner]
    @action(detail=True, methods=['patch'], url_path='delete-labels-from-task')
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


class AddDoersToTaskViewSet(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = UpdateTaskDoersSerializer
    permission_classes = [IsAdminUser | IsTaskBoardMember | IsTaskBoardAdmin | IsTaskBoardWorkSpaceOwner]
    @action(detail=True, methods=['patch'], url_path='add-doers-to-task')
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


class DeleteDoersFromTaskViewSet(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = UpdateTaskDoersSerializer
    permission_classes = [IsAdminUser | IsTaskBoardMember | IsTaskBoardAdmin | IsTaskBoardWorkSpaceOwner]
    @action(detail=True, methods=['patch'], url_path='delete-doers-from-task')
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


class GetTaskPreviewViewSet(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskPreviewSerializer
    permission_classes = [IsAdminUser | IsTaskBoardMember | IsTaskBoardAdmin | IsTaskBoardWorkSpaceOwner]
    @action(detail=True, methods=['get'])
    def preview(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GetTaskViewSet(GetTaskPreviewViewSet):
    serializer_class = GetTaskSerializer

    @action(detail=True, methods=['get'], url_path='get-task')
    def get_task(self, request, pk):
        return super().preview(request, pk)


class AddAttachmentToTaskViewSet(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [IsAdminUser | IsTaskBoardMember | IsTaskBoardAdmin | IsTaskBoardWorkSpaceOwner]
    @action(detail=True, methods=['patch'], url_path='add-attachment-to-task')
    def add_attachment_to_task(self, request, pk):
        task = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(task=task, user=request.user.profile)
        return Response(CreateTaskSerializer(instance=task).data, status=status.HTTP_200_OK)


class DeleteAttachmentFromTaskViewSet(viewsets.GenericViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [IsAdminUser | IsAttachmentBoardMember | IsAttachmentBoardAdmin | IsAttachmentBoardWorkSpaceOwner]
    @action(detail=True, methods=['delete'], url_path='delete-attachment-from-task')
    def delete_attachment_from_task(self, request, pk):
        at = self.get_object()
        at.delete()
        return Response(CreateTaskSerializer(instance=at.task).data, status=status.HTTP_200_OK)
