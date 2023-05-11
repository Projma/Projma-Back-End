from rest_framework import serializers
from retro.models import RetroSession


class CreateSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetroSession
        fields = ['id', 'board', 'attendees', 'admin', 'vote_limitation', 'retro_step']
        read_only_fields = ['id', 'attendees', 'admin', 'vote_limitation', 'retro_step']