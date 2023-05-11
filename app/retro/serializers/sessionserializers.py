from rest_framework import serializers
from retro.models import RetroSession


class CreateSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetroSession
        fields = ['id', 'board']
        read_only_fields = ['id']