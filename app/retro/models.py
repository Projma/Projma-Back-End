from django.db import models
from colorfield.fields import ColorField
from accounts.models import Profile
from board.models import Board
from workspaces.models import WorkSpace

# Create your models here.


class RetroSession(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='retro_sessions')
    attendees = models.ManyToManyField(Profile, related_name='retro_sessions')
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='administrating_retro_sessions')


class CardGroup(models.Model):
    name = models.CharField(max_length=64)
    retro_session = models.ForeignKey(RetroSession, on_delete=models.CASCADE, related_name='card_groups')


class RetroCard(models.Model):
    card_group = models.ForeignKey(CardGroup, on_delete=models.CASCADE, related_name='retro_cards')


class RetroReaction(models.Model):
    LIKE = 'LIKE'
    DISLIKE = 'DISLIKE'
    TYPE_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]
    type = models.CharField()
    card_group = models.ForeignKey(CardGroup, on_delete=models.CASCADE, related_name='retro_reactions')
