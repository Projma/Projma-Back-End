from django.db import models
from colorfield.fields import ColorField
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


class Board(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1000, blank=True, null=True)
    background_pic = models.ImageField(blank=True, null=True)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name='boards', null=True)
    admins = models.ManyToManyField(Profile, related_name='administrating_boards', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    members = models.ManyToManyField(Profile, related_name='boards', blank=True)
    is_starred = models.BooleanField(default=False)
    is_template = models.BooleanField(default=False)

    def save(self, **kwargs) -> None:
        is_template = kwargs.get('is_template')
        workspace = kwargs.get('workspace')
        print(is_template, self.is_template)
        print(workspace, self.workspace)
        if not self.is_template:
            if self.workspace is None:
                raise Exception("Board must have a workspace")
        else:
            if self.workspace is not None:
                raise Exception("Board template can't have a workspace")
        super().save(**kwargs)

    def reorder_tasklists(self, neworder):
        ids = [tl.id for tl in self.tasklists.all()]
        if len(neworder) != len(ids):
            raise Exception("Invalid Order")
        for pk in neworder:
            if pk not in ids:
                raise Exception("Invalid Order")

        for i in range(len(neworder)):
            pk = neworder[i]
            tl = self.tasklists.all().get(pk=pk)
            tl.order = i+1
            tl.save()

    def __str__(self) -> str:
        return f'{self.name}'


class TaskList(models.Model):
    title = models.CharField(max_length=256)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasklists', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    order = models.IntegerField(default=0, null=False)

    def save(self, *args, **kwargs):
        creating = False
        if self.pk == None:
            creating = True
        super().save(*args, **kwargs)
        if creating:
            self.order = self.pk
        return

    def __str__(self) -> str:
        return f'{self.title} - {self.board.name}'


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        self.out_of_estimate = self.spend - self.estimate
        super().save(*args, **kwargs)

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


class Label(models.Model):
    title = models.CharField(max_length=256)
    color = ColorField()
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='labels', blank=True, null=True)


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    user = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


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