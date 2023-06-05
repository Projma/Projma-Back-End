from django.db.models import Sum
from rest_framework import serializers
from retro.models import RetroSession, CardGroup, RetroCard, RetroReaction
from retro.serializers.cardserializer import RetroCardSerializer
from retro.serializers.groupserializer import CardGroupSerializer, DiscussCardGroupSerializer, GroupsWithCardsSerializer
from retro.serializers.reactionserializer import RetroReactionSerializer
from accounts.serializers import PublicInfoProfileSerializer


class CreateSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetroSession
        fields = ['id', 'board', 'attendees', 'admin', 'vote_limitation', 'retro_step']
        read_only_fields = ['id']


class IceBreakerStepSerializer(serializers.ModelSerializer):
    attendees = PublicInfoProfileSerializer(many=True)
    class Meta:
        model = RetroSession
        fields = ['id', 'board', 'attendees', 'admin', 'retro_step']
        read_only_fields = ['id', 'board', 'attendees', 'admin', 'retro_step']


class ReflectStepSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()
    is_retro_admin = serializers.SerializerMethodField()
    class Meta:
        model = RetroSession
        fields = ['id', 'board', 'admin', 'retro_step', 'cards', 'groups', 'is_retro_admin']
        read_only_fields = ['id', 'board', 'admin', 'is_retro_admin']

    def get_cards(self, obj:RetroSession):
        queryset = RetroCard.objects.select_related('card_group__retro_session').\
                    filter(card_group__retro_session__pk=obj.pk).all()
        serializer = RetroCardSerializer(queryset, many=True)
        return serializer.data

    def get_groups(self, obj:RetroSession):
        queryset = CardGroup.objects.filter(retro_session__pk=obj.pk).all()
        serializer = CardGroupSerializer(queryset, many=True)
        return serializer.data

    def get_is_retro_admin(self, obj:RetroSession):
        return self.context['request'].user.profile == obj.admin

class GroupStepSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    is_retro_admin = serializers.SerializerMethodField()

    class Meta:
        model = RetroSession
        fields = ['id', 'board', 'admin', 'retro_step', 'groups', 'is_retro_admin']
        read_only_fields = ['id', 'board', 'admin', 'is_retro_admin']

    def get_groups(self, obj:RetroSession):
        queryset = CardGroup.objects.filter(retro_session__pk=obj.pk).all()
        serializer = GroupsWithCardsSerializer(queryset, many=True)
        return serializer.data

    def get_is_retro_admin(self, obj:RetroSession):
        return self.context['request'].user.profile == obj.admin


class VoteStepSerializer(serializers.ModelSerializer):
    group_votes = serializers.SerializerMethodField()
    user_votes = serializers.SerializerMethodField()
    team_votes = serializers.SerializerMethodField()
    is_retro_admin = serializers.SerializerMethodField()

    class Meta:
        model = RetroSession
        fields = ['id', 'board', 'admin', 'retro_step', 'group_votes', 'user_votes', 'team_votes', 'is_retro_admin']
        read_only_fields = ['id', 'board', 'admin', 'is_retro_admin']

    def get_reactions(self, obj:RetroSession, all=False):
        queryset = RetroReaction.objects.filter(card_group__retro_session__pk=obj.pk)
        if not all:
            queryset = queryset.filter(reactor=self.context['request'].user.profile).all()
        return queryset

    def get_group_votes(self, obj:RetroSession):
        queryset = self.get_reactions(obj)
        serializer = RetroReactionSerializer(queryset, many=True)
        return serializer.data

    def get_user_votes(self, obj:RetroSession):
        queryset = self.get_reactions(obj)
        user_votes = queryset.aggregate(Sum('count'))
        votes = obj.vote_limitation
        if user_votes['count__sum']:
            votes = votes - user_votes['count__sum']
        return votes

    def get_team_votes(self, obj:RetroSession):
        queryset = self.get_reactions(obj, True)
        team_votes = queryset.aggregate(Sum('count'))
        votes = obj.vote_limitation * len(obj.attendees.all())
        if team_votes['count__sum']:
            votes = votes - team_votes['count__sum']
        return votes

    def get_is_retro_admin(self, obj:RetroSession):
        return self.context['request'].user.profile == obj.admin


class DiscussStepSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    is_retro_admin = serializers.SerializerMethodField()

    class Meta:
        model = RetroSession
        fields = ['id', 'retro_step', 'groups', 'is_retro_admin']
        read_only_fields = ['id', 'is_retro_admin']

    def get_groups(self, obj:RetroSession):
        cgs = obj.card_groups.all()
        serializer = DiscussCardGroupSerializer(cgs, many=True)
        data = sorted(serializer.data, key=lambda x:x['votes'], reverse=True)
        return data

    def get_is_retro_admin(self, obj:RetroSession):
        return self.context['request'].user.profile == obj.admin