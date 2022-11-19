from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import WorkSpace, Profile, Board

class WorkspaceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True,)
    class Meta:
        model = WorkSpace
        fields = ['id', 'name', 'description', 'type', 'created_at', 'owner']

    def create(self, validated_data):
        try:
            user = self.context['request'].user
        except:
            raise serializers.ValidationError("User not found")
        profile = get_object_or_404(Profile, user=user)
        validated_data['owner'] = profile
        return super().create(validated_data)


class BoardSerializer(serializers.ModelSerializer):
    workspace = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Board
        fields = ['name', 'description', 'workspace']