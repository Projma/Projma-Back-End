from django.db import models
from accounts.models import Profile
from board.models import TaskList

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=1000, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    estimate = models.FloatField(blank=True, null=True, default=0.0)
    spend = models.FloatField(blank=True, null=True, default=0.0)
    out_of_estimate = models.FloatField(blank=True, null=True)
    tasklist = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='tasks')
    labels = models.ManyToManyField(to='Label', related_name='tasks', blank=True)
    doers = models.ManyToManyField(to=Profile, related_name='tasks', blank=True)
    order = models.IntegerField(default=0, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        creating = self.pk == None
        self.out_of_estimate = self.spend - self.estimate
        super().save(*args, **kwargs)
        if creating:
            self.order = self.pk
            self.save()
        return

    def __str__(self) -> str:
        return f'{self.title}'


class Comment(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='comments')
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE, related_name='comments')
    reply_to = models.ForeignKey(to='Comment', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.text}'


class CheckList(models.Model):
    text = models.CharField(max_length=512)
    is_done = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='checklists')

    def __str__(self) -> str:
        return super().__str__()


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    user = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
