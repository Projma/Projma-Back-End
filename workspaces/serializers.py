from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import WorkSpace, Profile, Board

class WorkspaceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    boards = serializers.PrimaryKeyRelatedField(read_only = True, many=True)
    class Meta:
        model = WorkSpace
        fields = ['id', 'name', 'description', 'type', 'created_at', 'updated_at', 'owner', 'members', 'boards']

    def create(self, validated_data):
        try:
            user = self.context['request'].user
        except:
            raise serializers.ValidationError("User not found")
        profile = get_object_or_404(Profile, user=user)
        validated_data['owner'] = profile
        return super().create(validated_data)


class BoardSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    workspace = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'background_pic', 'workspace', 'admins', 
                    'created_at', 'updated_at', 'members', 'tasklists']

    def create(self, validated_data):
        request = self.context['request']
        workspace_id = self.context.get('workspace_id')
        if str(workspace_id) in request.path:
            workspace = get_object_or_404(WorkSpace, pk=workspace_id)
            validated_data['workspace'] = workspace
            return super().create(validated_data)
        elif workspace_id is None:
            return super().create(validated_data)

