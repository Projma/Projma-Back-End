from datetime import timezone
from django.db import models
from django.core.exceptions import ValidationError
from colorfield.fields import ColorField
from board.models import Board
from django.db.models import Q
from datetime import timedelta
from accounts.models import Profile
from django.core.validators import MinLengthValidator


class SimpleCalendar(models.Model):
    board = models.OneToOneField(to=Board, on_delete=models.CASCADE, related_name='calendar')

    def __str__(self) -> str:
        return f'{self.board.name} calendar'

    def get_meetings(self, from_date=None, until_date=None, contain_repeats=False):
        single_meets = self.meetings.filter(repeat=0)
        periodic_meets = self.meetings.all().exclude(repeat=0)
        if not (from_date is None):
            single_meets = single_meets.filter(from_date__gte=from_date)
            periodic_meets = periodic_meets.exclude(until_date__lt=from_date)
        if not (until_date is None):
            single_meets = single_meets.filter(until_date__lte=until_date)
            periodic_meets = periodic_meets.exclude(from_date__gt=until_date)
        if contain_repeats and not (from_date is None or until_date is None):
            repeats = []
            for meet in periodic_meets:
                repeats += meet.duplicate(from_date, until_date)
            periodic_meets = repeats

        return list(single_meets) + list(periodic_meets)




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

    title = models.CharField(max_length=110, validators=[MinLengthValidator(3)])
    description = models.TextField(blank=True, null=True)
    start = models.TimeField()
    end = models.TimeField()
    from_date = models.DateField()
    until_date = models.DateField()
    repeat = models.PositiveIntegerField(default=0)
    link = models.CharField(max_length=512, blank=True, null=True)
    room_id = models.IntegerField(null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=NOTSTARTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    creator = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='created_meetings')
    calendar = models.ForeignKey(to=SimpleCalendar, on_delete=models.CASCADE, related_name='meetings')
    color = ColorField()

    def save(self, **kwargs) -> None:
        creating = self.pk is None
        if creating:
            self.status = self.NOTSTARTED
            self.link = None
            self.room_id = None
        super().save(**kwargs)

    def to_single(self, date):
        singlemeet = Meeting()
        singlemeet.id = self.id
        singlemeet.title = self.title
        singlemeet.description = self.description
        singlemeet.start = self.start
        singlemeet.end = self.end
        singlemeet.from_date = date
        singlemeet.until_date = date
        singlemeet.repeat = 0
        singlemeet.link = self.link
        singlemeet.room_id = self.room_id
        singlemeet.status = self.status
        singlemeet.created_at = self.created_at
        singlemeet.updated_at = self.updated_at
        singlemeet.creator = self.creator
        singlemeet.calendar = self.calendar
        singlemeet.color = self.color
        return singlemeet

    def duplicate(self, from_date, until_date):
        cur_date = self.from_date
        duplicates = []
        while cur_date < from_date:
            cur_date += timedelta(days=self.repeat)
        while cur_date <= until_date and cur_date <= self.until_date:
            duplicates.append(self.to_single(cur_date))
            cur_date += timedelta(days=self.repeat)
        return duplicates

    