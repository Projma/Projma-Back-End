from django.shortcuts import get_object_or_404
from rest_framework import serializers
from ..models import CheckList, Task

class CreateOrReadCheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = ['id', 'text', 'is_done']
        read_only_fields = ['id', 'is_done']


class UpdateCheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = ['id', 'text', 'is_done']
        read_only_fields = ['id']
