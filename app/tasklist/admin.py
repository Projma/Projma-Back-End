from django.contrib import admin
from tasklist.models import TaskList
# Register your models here.

class TaskListAdmin(admin.ModelAdmin):
    model = TaskList
    fields = ['id', 'title', 'board', 'order']
    readonly_fields = ['id']

admin.site.register(TaskList, TaskListAdmin)
