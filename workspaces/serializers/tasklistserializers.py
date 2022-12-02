from django.shortcuts import get_object_or_404
from rest_framework import serializers
from accounts.serializers import *
from ..models import *


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskList
        fields = ['id', 'title', 'board', 'order','tasks']
        read_only_fields = ['id', 'board', 'order', 'tasks']


class ReorderTaskListSerializer(serializers.Serializer):
    order = serializers.ListField(child = serializers.IntegerField())

