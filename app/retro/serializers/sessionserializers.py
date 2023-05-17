from rest_framework import serializers
from retro.models import RetroSession
from accounts.serializers import PublicInfoProfileSerializer


class CreateSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetroSession
        fields = ['id', 'board', 'attendees', 'admin', 'vote_limitation', 'retro_step']
        read_only_fields = ['id']


class IceBreakerSerializer(serializers.ModelSerializer):
    attendees = PublicInfoProfileSerializer(many=True)
    class Meta:
        model = RetroSession
        fields = ['id', 'board', 'attendees', 'admin', 'retro_step']
        read_only_fields = ['id', 'board', 'attendees', 'admin', 'retro_step']