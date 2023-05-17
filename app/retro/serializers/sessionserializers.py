from rest_framework import serializers
from retro.models import RetroSession, CardGroup, RetroCard
from retro.serializers.cardserializer import RetroCardSerializer
from retro.serializers.groupserializer import CardGroupSerializer
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


class ReflectSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()
    class Meta:
        model = RetroSession
        fields = ['id', 'board', 'admin', 'retro_step', 'cards', 'groups']

    def get_cards(self, obj:RetroSession):
        queryset = RetroCard.objects.select_related('card_group__retro_session').\
                    filter(card_group__retro_session__pk=obj.pk).all()
        serializer = RetroCardSerializer(queryset, many=True)
        return serializer.data

    def get_groups(self, obj:RetroSession):
        queryset = CardGroup.objects.filter(retro_session__pk=obj.pk).all()
        serializer = CardGroupSerializer(queryset, many=True)
        return serializer.data