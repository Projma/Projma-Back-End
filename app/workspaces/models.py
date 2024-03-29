from django.db import models
from accounts.models import Profile
from django.db.models import signals
from django.dispatch import receiver

# Create your models here.
class WorkSpace(models.Model):
    TYPE_CHOICES = [
        ("education", "آموزشی"),
        ("marketing", "بازاریابی"),
        ("small business", "سرمایه گذاری کوچک"),
        ("operations", "عملیاتی"),
        ("engineering-it", "مهندسی و IT"),
        ("finance", "مالی"),
        ("human resources", "منابع انسانی"),
        ("other", "سایر"),
    ]

    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1000, blank=True, null=True)
    type = models.CharField(max_length=256, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owning_workspaces')
    members = models.ManyToManyField(to=Profile, related_name='workspaces', blank=True)

    def __str__(self) -> str:
        return f'{self.name} - {self.owner.user.username}'

    # def save(self, *args, **kwargs) -> None:
    #     super().save(*args, **kwargs)
    #     if self.owner not in self.members.all():
    #         self.members.add(self.owner)
    #     # super().save(*args, **kwargs)
    #     return




# class BoardTemplate(models.Model):
#     name = models.CharField(max_length=256, unique=True)
#     description = models.CharField(max_length=1000, blank=True, null=True)
#     background_pic = models.ImageField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateField(auto_now=True)


# class TaskLabel(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     label = models.ForeignKey(Label, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('task', 'label')


# class WorksOn(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('profile', 'task')


# class BoardAdmin(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     board = models.ForeignKey(Board, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('profile', 'board')


# class MemberShip(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     board = models.ForeignKey(Board, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('profile', 'board')