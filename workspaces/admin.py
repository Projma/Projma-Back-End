from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.
class WorkSpaceAdmin(admin.ModelAdmin):
    model = WorkSpace
    form = WorkSpaceForm


class BoardAdmin(admin.ModelAdmin):
    model = Board
    form = BoardForm


class TaskListAdmin(admin.ModelAdmin):
    pass


class TaskAdmin(admin.ModelAdmin):
    pass


class CheckListAdmin(admin.ModelAdmin):
    pass


class LabelAdmin(admin.ModelAdmin):
    pass


class FileAdmin(admin.ModelAdmin):
    pass

admin.site.register(WorkSpace, WorkSpaceAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(TaskList, TaskListAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(CheckList, CheckListAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(File, FileAdmin)
