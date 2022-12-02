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
        if profile in board.admins.all() or profile == board.workspace.owner:
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
        fields = ['id', 'title', 'board', 'order','tasks']
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


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'created_at', 'updated_at', 'title', 'description', 'start_date', 'end_date', \
                  'estimate', 'spend', 'out_of_estimate', 'tasklist', 'labels', 'doers']
        read_only_fields = ['id', 'created_at', 'updated_at', 'description', 'start_date', 'end_date', \
                  'estimate', 'spend', 'out_of_estimate', 'tasklist', 'labels', 'doers']
    
    def validate(self, data):
        print(data)
        if self.instance:
            board = self.instance.tasklist.board
        return data


class UpdateTaskSerializer(serializers.ModelSerializer):
    doers = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all(), pk_field=serializers.IntegerField())
    labels = serializers.PrimaryKeyRelatedField(many=True, queryset=Label.objects.all())
    tasklist = serializers.PrimaryKeyRelatedField(queryset=TaskList.objects.all())
    class Meta:
        model = Task
        fields = ['id', 'created_at', 'updated_at', 'title', 'description', 'start_date', 'end_date', \
                  'estimate', 'spend', 'out_of_estimate', 'tasklist', 'labels', 'doers']
        read_only_fields = ['id', 'created_at', 'updated_at', 'out_of_estimate',]
        
    def validate_doers(self, value):
        if self.instance:
            board = self.instance.tasklist.board
            for doer in value:
                if doer not in board.members.all():
                    raise serializers.ValidationError({"doers": "username = " + str(doer.username) + " does not exist in this board"})
        return value
    
    def validate_labels(self, value):
        if self.instance:
            board = self.instance.tasklist.board
            for label in value:
                if label not in board.labels.all():
                    raise serializers.ValidationError({"labels": "label id = " + str(label.id) + " does not exist in this board"})
        return value
    
    def validate_tasklist(self, value):
        if self.instance:
            board = self.instance.tasklist.board
            if value not in board.tasklists.all():
                raise serializers.ValidationError({"tasklist": "tasklist does not exist in this board"})
        return value