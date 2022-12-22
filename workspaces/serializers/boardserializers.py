from django.shortcuts import get_object_or_404
from rest_framework import serializers
from accounts.serializers import *
from .tasklistserializers import *
from .labelserializers import *
from ..models import *


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


class BoardChangeRoleSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    role = serializers.CharField()
    class Meta:
        model = Profile
        fields = ['user_id', 'role']

    def validate_role(self, value):
        if value not in ['Admin', 'Member']:
            raise serializers.ValidationError('Invalid role')
        return value


class BoardOverviewSerializer(serializers.ModelSerializer):
    workspace = serializers.PrimaryKeyRelatedField(read_only=True)
    tasklists = TaskListOverviewSerializer(read_only=True, many=True)
    labels = LabelSerializer(read_only=True, many=True)
    admins = ProfileOverviewSerializer(read_only=True, many=True)
    members = ProfileOverviewSerializer(read_only=True, many=True)
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'background_pic', 'workspace', 'admins', 
                    'created_at', 'updated_at', 'members', 'tasklists', 'labels']
        read_only_fields = ['id', 'workspace', 'labels']


class BoardIdsSerializer(serializers.Serializer):
    board_ids = serializers.ListField(child = serializers.IntegerField(), read_only=True)