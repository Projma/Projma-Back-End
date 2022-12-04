from django.shortcuts import get_object_or_404
from rest_framework import serializers
from accounts.serializers import *
from .labelserializers import *
from ..models import *

class TaskPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'tasklist', 'labels', 'doers']
        read_only_fields = ['id', 'title', 'tasklist', 'labels', 'doers']


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
        read_only_fields = ['id', 'created_at', 'updated_at', 'out_of_estimate']
        
    def validate_doers(self, value):
        if self.instance:
            board = self.instance.tasklist.board
            for doer in value:
                if doer not in board.members.all():
                    raise serializers.ValidationError({"doers": "username = " + str(doer.user.username) + " does not exist in this board"})
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


class UpdateTaskLabelsSerializer(UpdateTaskSerializer):
    class Meta:
        model = Task
        fields = ['id', 'created_at', 'updated_at', 'title', 'description', 'start_date', 'end_date', \
                  'estimate', 'spend', 'out_of_estimate', 'labels', 'tasklist', 'doers']
        read_only_fields = ['id', 'created_at', 'updated_at', 'title', 'description', 'start_date', 'end_date', \
                  'estimate', 'spend', 'out_of_estimate', 'tasklist', 'doers']
    
class UpdateTaskDoersSerializer(UpdateTaskSerializer):
    class Meta:
        model = Task
        fields = ['id', 'created_at', 'updated_at', 'title', 'description', 'start_date', 'end_date', \
                  'estimate', 'spend', 'out_of_estimate', 'doers']
        read_only_fields = ['id', 'created_at', 'updated_at', 'title', 'description', 'start_date', 'end_date', \
                  'estimate', 'spend', 'out_of_estimate', 'tasklist']
