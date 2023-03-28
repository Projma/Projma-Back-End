from django.db import models
from board.models import Board
# Create your models here.


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
