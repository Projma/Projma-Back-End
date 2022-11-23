from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import WorkSpace, Profile, Board

class WorkspaceSerializer(serializers.ModelSerializer):
    boards = serializers.PrimaryKeyRelatedField(read_only = True, many=True)
    class Meta:
        model = WorkSpace
        fields = ['id', 'name', 'description', 'type', 'created_at', 'updated_at', 'owner', 'members', 'boards']
        read_only_fields = ['id', 'owner']


class BoardSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    workspace = serializers.PrimaryKeyRelatedField(read_only=True)
    tasklists = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'background_pic', 'workspace', 'admins', 
                    'created_at', 'updated_at', 'members', 'tasklists']


