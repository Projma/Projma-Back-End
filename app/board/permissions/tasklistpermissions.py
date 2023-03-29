from board.permissions.boardpermissions import *


class IsTaskListBoardMember(IsBoardMember):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.board)


class IsTaskListBoardAdmin(IsBoardAdmin):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.board)


class IsTaskListBoardWorkSpaceOwner(IsBoardWorkSpaceOwner):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.board)

