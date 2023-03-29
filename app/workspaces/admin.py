from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.
class WorkSpaceAdmin(admin.ModelAdmin):
    model=WorkSpace
    fields = ['id', 'name', 'description', 'type', 'owner', 'members']
    readonly_fields = ['id']


admin.site.register(WorkSpace, WorkSpaceAdmin)

