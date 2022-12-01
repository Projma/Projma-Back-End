from django.shortcuts import get_object_or_404
from rest_framework import serializers
from accounts.serializers import *
from .models import *

class WorkSpaceOwnerSerializer(serializers.ModelSerializer):
    boards = serializers.PrimaryKeyRelatedField(read_only = True, many=True)
    class Meta:
        model = WorkSpace
        fields = ['id', 'name', 'description', 'type', 'created_at', 'updated_at', 'owner', 'members', 'boards']
        read_only_fields = ['id', 'owner']


class WorkSpaceMemberSerializer(serializers.ModelSerializer):
    boards = serializers.PrimaryKeyRelatedField(read_only = True, many=True)
    class Meta:
        model = WorkSpace
        fields = ['id', 'name', 'description', 'type', 'owner', 'members', 'boards']
        read_only_fields = ['id', 'name', 'description', 'type', 'owner', 'members']


class BoardAdminSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    workspace = serializers.PrimaryKeyRelatedField(read_only=True)
    tasklists = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'background_pic', 'workspace', 'admins', 
                    'created_at', 'updated_at', 'members', 'tasklists', 'labels']
        read_only_fields = ['id', 'workspace', 'labels']


class BoardMemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    tasklists = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'background_pic', 'admins', 'members', 'tasklists', 'labels']
        read_only_fields = ['id', 'workspace', 'labels']

class BoardMembersSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    role = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['user', 'birth_date', 'bio', 'phone', 'profile_pic', 'role']

    def get_role(self, profile: Profile):
        board_id = int(self.context.get('board'))
        board = Board.objects.get(pk=board_id)
        if profile in board.admins.all():
            return 'Admin'
        elif profile in board.members.all():
            return 'Member'

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'title', 'color', 'board']
        read_only_fields = ['id', 'board']

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskList
        fields = ['id', 'title', 'board', 'order',' tasks']
        read_only_fields = ['id', 'board', 'order', 'tasks']


class ReorderTaskListSerializer(serializers.Serializer):
    order = serializers.ListField(child = serializers.IntegerField())


class BoardOverviewSerializer(serializers.ModelSerializer):
    workspace = serializers.PrimaryKeyRelatedField(read_only=True)
    tasklists = TaskListSerializer(read_only=True, many=True)
    labels = LabelSerializer(read_only=True, many=True)
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'background_pic', 'workspace', 'admins', 
                    'created_at', 'updated_at', 'members', 'tasklists', 'labels']
        read_only_fields = ['id', 'workspace', 'labels']

# class FullTaskListSerializer(serializers.ModelSerializer):
#     tasks = Task
#     class Meta:
#         model = TaskList
#         fields = ['id', 'title', 'board', 'order',' tasks']
#         read_only_fields = ['id', 'board', 'order', 'tasks']

