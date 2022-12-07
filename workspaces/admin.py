from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.
class WorkSpaceAdmin(admin.ModelAdmin):
    model = WorkSpace


class BoardAdmin(admin.ModelAdmin):
    model = Board


class TaskListAdmin(admin.ModelAdmin):
    pass


class TaskAdmin(admin.ModelAdmin):
    model = Task
    fields = ['title', 'description', 'start_date', 'end_date', \
                'estimate', 'spend', 'out_of_estimate', 'tasklist', 'labels', 'doers', 'attachments']
    read_only_fields = ['id', 'created_at', 'updated_at']


class CheckListAdmin(admin.ModelAdmin):
    pass


class LabelAdmin(admin.ModelAdmin):
    pass


class AttachmentAdmin(admin.ModelAdmin):
    pass

admin.site.register(WorkSpace, WorkSpaceAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(TaskList, TaskListAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(CheckList, CheckListAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Attachment, AttachmentAdmin)
