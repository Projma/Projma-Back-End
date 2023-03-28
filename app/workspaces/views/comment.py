from django.shortcuts import get_object_or_404 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from ..models import *
from ..serializers.commentserializers import *
from ..permissions.commentpermissions import *
from task.permissions.taskpermissions import *
from task.models import Task
from accounts.serializers import *

class NewCommentViewset(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser | IsTaskBoardMember | IsTaskBoardAdmin | IsTaskBoardWorkSpaceOwner]
    @action(detail=True, methods=['post'], url_path='new-comment')
    def new_comment(self, request, pk):
        task = self.get_object()
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(task=task,sender=request.user.profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReplyCommentViewSet(viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser | IsCommentBoardMember | IsCommentBoardAdmin | IsCommentBoardWorkSpaceOwner]
    @action(detail=True, methods=['post'], url_path='reply-comment')
    def reply_comment(self, request, pk):
        rpcom = self.get_object()
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(task=rpcom.task, sender=request.user.profile, reply_to=rpcom)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EditCommentViewSet(viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser | IsCommentSender]
    @action(detail=True, methods=['patch'], url_path='eddit-comment')
    def eddit_comment(self, request, pk):
        com = self.get_object()
        serializer = CommentSerializer(instance=com, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DeleteCommentViewSet(viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser | IsCommentSender | IsCommentBoardAdmin | IsCommentBoardWorkSpaceOwner]
    @action(detail=True, methods=['delete'], url_path='delete-comment')
    def delete_comment(self, request, pk):
        com = self.get_object()
        com.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
