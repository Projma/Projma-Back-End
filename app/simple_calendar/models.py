from datetime import timezone
from django.db import models
from django.core.exceptions import ValidationError
from colorfield.fields import ColorField
from board.models import Board
from accounts.models import Profile

# Create your models here.

class SimpleCalendar(models.Model):
    board = models.OneToOneField(to=Board, on_delete=models.CASCADE, related_name='calendar')

    def __str__(self) -> str:
        return f'{self.board.name} calendar'


class Event(models.Model):
    Error_Messages = ["you can't select an event type and enter a custom event type together.",
                      "you must select an event type or enter a custom event type."]
    EVENT_TYPE_CHOICES = [
        ('task', 'فعالیت'),
        ('holidays', 'تعطیلات'),
        ('meeting', 'جلسه')
    ]

    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    event_time = models.DateTimeField()
    repeat_duration = models.PositiveIntegerField(default=0)
    event_color = ColorField()
    event_type = models.CharField(choices=EVENT_TYPE_CHOICES, blank=True, max_length=64)
    custom_event_type = models.CharField(max_length=64, blank=True)
    calendar = models.ForeignKey(to=SimpleCalendar, on_delete=models.CASCADE, related_name='events')

    def save(self, *args, **kwargs) -> None:
        self.event_time = self.event_time.astimezone(timezone.utc)
        if self.event_type and self.custom_event_type:
            raise ValidationError(self.Error_Messages[0])
        elif not self.event_type and not self.custom_event_type:
            raise ValidationError(self.Error_Messages[1])
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.title}'

class Meeting(models.Model):
    NOTSTARTED = 'NOTSTARTED'
    HOLDING = 'HOLDONG'
    FINISHED = 'FINISHED'
    STATUS_CHOICES = [
        (NOTSTARTED, 'Not Started'),
        (HOLDING, 'Holding'),
        (FINISHED, 'Finished')
    ]

    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    from_date = models.DateField()
    until_date = models.DateField()
    repeat = models.PositiveIntegerField(default = 0)
    link = models.CharField(max_length=512)
    status = models.CharField(max_length=10, choices = STATUS_CHOICES, default = NOTSTARTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    creator = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='created_meetings')
    