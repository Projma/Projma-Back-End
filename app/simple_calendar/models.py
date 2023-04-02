from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    event_time = models.DateTimeField()
    repeat_duration = models.PositiveIntegerField(default=0)
    
    def __str__(self) -> str:
        return f'{self.title}'