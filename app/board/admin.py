from django.contrib import admin
from board.models import Board
# Register your models here.


class BoardAdmin(admin.ModelAdmin):
    model = Board
    fields = ['id', 'name', 'description', 'background_pic', 'workspace', 'admins', 'members', 'is_starred']
    readonly_fields = ['id']


admin.site.register(Board, BoardAdmin)