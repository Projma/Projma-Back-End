from django.contrib import admin
from board.models import Board, LogUserRecentBoards
# Register your models here.


class BoardAdmin(admin.ModelAdmin):
    model = Board
    fields = ['id', 'name', 'description', 'background_pic', 'workspace', 'admins', 'members', 'is_starred']
    readonly_fields = ['id']


class LogUserRecentBoardsAdmin(admin.ModelAdmin):
    model = LogUserRecentBoards
    fields = ['id', 'profile', 'board', 'lastseen']
    readonly_fields = ['id', 'profile', 'board', 'lastseen']


admin.site.register(LogUserRecentBoards, LogUserRecentBoardsAdmin)
admin.site.register(Board, BoardAdmin)