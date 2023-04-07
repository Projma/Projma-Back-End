from django.db import models
from colorfield.fields import ColorField
from accounts.models import Profile
from workspaces.models import WorkSpace

# Create your models here.

class Board(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1000, blank=True, null=True)
    background_pic = models.ImageField(blank=True, null=True, upload_to='background_pics/')
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


class LogUserRecentBoards(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    lastseen = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('profile', 'board',)

    @classmethod
    def set_lastseen(cls, profile, board):
        log, created = cls.objects.get_or_create(profile=profile, board=board)
        log.save()
    
    def __str__(self):
        return f'{self.profile.user.username} - {self.board.name}'


class TaskList(models.Model):
    title = models.CharField(max_length=256)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasklists', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    order = models.IntegerField(default=0, null=False)

    def save(self, *args, **kwargs):
        creating = self.pk==None
        super().save(*args, **kwargs)
        if creating:
            self.order = self.pk
            self.save()
        return

    def reorder_tasks(self, neworder):
        ids = [t.id for t in self.tasks.all()]
        if len(neworder) != len(ids):
            raise Exception("Invalid Order")
        for pk in neworder:
            if pk not in ids:
                raise Exception("Invalid Order")

        for i in range(len(neworder)):
            pk = neworder[i]
            t = self.tasks.all().get(pk=pk)
            t.order = i+1
            t.save()

    def __str__(self) -> str:
        return f'{self.title} - {self.board.name}'


class Label(models.Model):
    title = models.CharField(max_length=256)
    color = ColorField()
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='labels', blank=True, null=True)

