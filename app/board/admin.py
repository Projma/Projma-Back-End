from django.contrib import admin
from board.models import Board, LogUserRecentBoards, TaskList
# Register your models here.


class BoardAdmin(admin.ModelAdmin):
    model = Board
    fields = ['id', 'name', 'description', 'background_pic', 'workspace', 'admins', 'members', 'is_starred']
    readonly_fields = ['id']


class LogUserRecentBoardsAdmin(admin.ModelAdmin):
    model = LogUserRecentBoards
    fields = ['id', 'profile', 'board', 'lastseen']
    readonly_fields = ['id', 'profile', 'board', 'lastseen']

class TaskListAdmin(admin.ModelAdmin):
    model = TaskList
    fields = ['id', 'title', 'board', 'order']
    readonly_fields = ['id']

admin.site.register(TaskList, TaskListAdmin)


admin.site.register(LogUserRecentBoards, LogUserRecentBoardsAdmin)
admin.site.register(Board, BoardAdmin)