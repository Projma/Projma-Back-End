from django.contrib import admin
from task.models import Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    model = Task
    fields = ['id', 'title', 'description', 'start_date', 'end_date', \
                'estimate', 'spend', 'out_of_estimate', 'tasklist', 'labels', 'doers', 'order']
    readonly_fields = ['id', 'created_at', 'updated_at', 'out_of_estimate']


admin.site.register(Task, TaskAdmin)
