from django.shortcuts import get_object_or_404
from rest_framework import serializers
from accounts.serializers import *
from ..models import *


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
