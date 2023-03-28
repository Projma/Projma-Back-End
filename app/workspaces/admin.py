from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.
class WorkSpaceAdmin(admin.ModelAdmin):
    model=WorkSpace
    fields = ['id', 'name', 'description', 'type', 'owner', 'members']
    readonly_fields = ['id']


class TaskListAdmin(admin.ModelAdmin):
    model = TaskList
    fields = ['id', 'title', 'board', 'order']
    readonly_fields = ['id']


class CheckListAdmin(admin.ModelAdmin):
    model = CheckList
    fields = ['id', 'text', 'is_done', 'task']
    readonly_fields = ['id']


class LabelAdmin(admin.ModelAdmin):
    model = Label
    fields = ['id', 'title', 'color', 'board']
    readonly_fields = ['id']


class AttachmentAdmin(admin.ModelAdmin):
    model = Attachment
    fields = ['id', 'file', 'task', 'user']
    readonly_fields = ['id']


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    fields = ['id', 'text', 'sender', 'task', 'reply_to', 'created_at', 'updated_at']
    readonly_fields = ['id', 'created_at', 'updated_at']

class LogUserRecentBoardsAdmin(admin.ModelAdmin):
    model = LogUserRecentBoards
    fields = ['id', 'profile', 'board', 'lastseen']
    readonly_fields = ['id', 'profile', 'board', 'lastseen']


admin.site.register(WorkSpace, WorkSpaceAdmin)
admin.site.register(TaskList, TaskListAdmin)
admin.site.register(CheckList, CheckListAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(LogUserRecentBoards, LogUserRecentBoardsAdmin)
