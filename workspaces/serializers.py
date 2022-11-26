from django.shortcuts import get_object_or_404
from rest_framework import serializers
from accounts.serializers import *
from .models import WorkSpace, Profile, Board

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
                    'created_at', 'updated_at', 'members', 'tasklists']
        read_only_fields = ['id', 'workspace']


class BoardMemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    tasklists = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'background_pic', 'admins', 'members', 'tasklists']


class BoardMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    role = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['user', 'birth_date', 'bio', 'phone', 'profile_pic', 'role']

    def get_role(self, profile: Profile):
        print('context::::::;', self.context)
        board_id = int(self.context.get('board'))
        board = Board.objects.get(pk=board_id)
        if profile in board.admins.all():
            return 'Admin'
        elif profile in board.members.all():
            return 'Member'