from .boardpermissions import *

class IsCheckListBoardMember(IsBoardMember):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.task.tasklist.board)


class IsCheckListBoardAdmin(IsBoardAdmin):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.task.tasklist.board)


class IsCheckListBoardWorkSpaceOwner(IsBoardWorkSpaceOwner):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.task.tasklist.board)