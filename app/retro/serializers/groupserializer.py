from rest_framework import serializers
from retro.models import CardGroup


class CardGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardGroup
        fields = ['id', 'name', 'retro_session', 'is_discussed']