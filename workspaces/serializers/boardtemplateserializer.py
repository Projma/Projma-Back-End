from rest_framework import serializers
from ..models import BoardTemplate
from .boardserializers import TaskListOverviewSerializer
from .labelserializers import LabelSerializer


class BoardTemplateSerializer(serializers.ModelSerializer):
    tasklists = TaskListOverviewSerializer(read_only=True, many=True)
    labels = LabelSerializer(read_only=True, many=True)
    class Meta:
        model = BoardTemplate
        fields = ['id', 'name', 'description', 'background_pic', 'created_at', 'updated_at', 'tasklists', 'labels']