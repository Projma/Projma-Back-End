from django.shortcuts import get_object_or_404
from rest_framework import serializers
from accounts.serializers import *
from ..models import *
from workspaces.serializers.taskserializers import *


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskList
        fields = ['id', 'title', 'board', 'order','tasks']
        read_only_fields = ['id', 'board', 'order', 'tasks']


class ReorderTaskListsSerializer(serializers.Serializer):
    order = serializers.ListField(child = serializers.IntegerField())


class TaskListOverviewSerializer(serializers.ModelSerializer):
    tasks = TaskOverviewSerializer(read_only=True, many=True)
    class Meta:
        model = TaskList
        fields = ['id', 'title', 'board', 'order','tasks']
        read_only_fields = ['id', 'board', 'order', 'tasks']