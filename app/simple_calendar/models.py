from django.db import models
from django.core.exceptions import ValidationError
from colorfield.fields import ColorField

# Create your models here.

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
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

    def clean(self) -> None:
        super().clean()
        if self.event_type and self.custom_event_type:
            raise ValidationError("you can't select an event type and enter a custom event type together.")
        elif not self.event_type and not self.custom_event_type:
            raise ValidationError("you must select an event type or enter a custom event type.")

    def __str__(self) -> str:
        return f'{self.title}'