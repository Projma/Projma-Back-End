from django.db import models
from colorfield.fields import ColorField
from accounts.models import Profile
from board.models import Board
from workspaces.models import WorkSpace

# Create your models here.


class RetroSession(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='retro_sessions', null=True)
    attendees = models.ManyToManyField(Profile, related_name='retro_sessions')
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='administrating_retro_sessions', null=True)


class CardGroup(models.Model):
    name = models.CharField(max_length=256)
    retro_session = models.ForeignKey(RetroSession, on_delete=models.CASCADE, related_name='card_groups')


class RetroCard(models.Model):
    card_group = models.ForeignKey(CardGroup, on_delete=models.CASCADE, related_name='retro_cards', null=True)
    text = models.CharField(max_length=256)
    is_positive = models.BooleanField()

    def init_group(self, session_id):
        session = RetroSession.objects.get(session_id)
        cg = CardGroup.objects.create(name=self.text, retro_session=session)
        self.card_group = cg
        self.save()

class RetroReaction(models.Model):
    LIKE = 'LIKE'
    DISLIKE = 'DISLIKE'
    TYPE_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]
    type = models.CharField(max_length=7)
    card_group = models.ForeignKey(CardGroup, on_delete=models.CASCADE, related_name='retro_reactions')
