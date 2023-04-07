from django.contrib import admin
from task.models import Task, CheckList, Comment, Attachment

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    model = Task
    fields = ['id', 'title', 'description', 'start_date', 'end_date', \
                'estimate', 'spend', 'out_of_estimate', 'tasklist', 'labels', 'doers', 'order']
    readonly_fields = ['id', 'created_at', 'updated_at', 'out_of_estimate']


class CheckListAdmin(admin.ModelAdmin):
    model = CheckList
    fields = ['id', 'text', 'is_done', 'task']
    readonly_fields = ['id']


class AttachmentAdmin(admin.ModelAdmin):
    model = Attachment
    fields = ['id', 'file', 'task', 'user']
    readonly_fields = ['id']


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    fields = ['id', 'text', 'sender', 'task', 'reply_to', 'created_at', 'updated_at']
    readonly_fields = ['id', 'created_at', 'updated_at']


admin.site.register(Task, TaskAdmin)
admin.site.register(CheckList, CheckListAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Comment, CommentAdmin)