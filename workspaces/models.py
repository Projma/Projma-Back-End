from django.db import models
from accounts.models import Profile


# Create your models here.
class WorkSpace(models.Model):
    TYPE_CHOICES = [
        ("education", "Education"),
        ("marketing", "Marketing"),
        ("small business", "Small Business"),
        ("sales & crm", "Sales & CRM"),
        ("operations", "Operations"),
        ("engineering-it", "Engineering IT"),
        ("finance", "Finance"),
        ("human resources", "Human Resources"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1000, blank=True, null=True)
    type = models.CharField(max_length=256, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Board(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1000, blank=True, null=True)
    background_pic = models.URLField(max_length=1000, blank=True, null=True)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)