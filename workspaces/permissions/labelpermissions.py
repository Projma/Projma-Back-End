from .boardpermissions import *

class IsLabelBoardMember(IsBoardMember):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.board)


class IsLabelBoardAdmin(IsBoardAdmin):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.board)


class IsLabelBoardWorkSpaceOwner(IsBoardWorkSpaceOwner):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.board)
