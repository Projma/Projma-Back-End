from rest_framework import serializers
from retro.models import RetroCard


class RetroCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetroCard
        fields = ['id', 'card_group', 'text', 'is_positive']
        read_only_fields = ['id']

class SimpleRetroCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetroCard
        fields = ['id', 'text']