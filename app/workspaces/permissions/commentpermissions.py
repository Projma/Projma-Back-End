from .boardpermissions import *


class IsCommentBoardMember(IsBoardMember):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.task.tasklist.board)


class IsCommentBoardAdmin(IsBoardAdmin):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.task.tasklist.board)


class IsCommentBoardWorkSpaceOwner(IsBoardWorkSpaceOwner):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.task.tasklist.board)


class IsCommentSender(IsCommentBoardMember):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj) and obj.sender == request.user.profile