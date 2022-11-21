from django.contrib import admin
from .models import *
# Register your models here.
class WorkspaceAdmin(admin.ModelAdmin):
    pass


class BoardAdmin(admin.ModelAdmin):
    pass


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

admin.site.register(Workspace, WorkspaceAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(TaskList, TaskListAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(CheckList, CheckListAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(File, FileAdmin)
