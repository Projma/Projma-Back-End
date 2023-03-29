from rest_framework import serializers
# from ..models import Board
from board.models import Board
from board.serializers.labelserializers import LabelSerializer
from board.serializers.tasklistserializers import TaskListOverviewSerializer



class BoardTemplateSerializer(serializers.ModelSerializer):
    tasklists = TaskListOverviewSerializer(read_only=True, many=True)
    labels = LabelSerializer(read_only=True, many=True)
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'background_pic', 'created_at', 'updated_at', 'tasklists', 'labels']