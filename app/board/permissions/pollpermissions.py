from board.permissions.boardpermissions import *


class IsPollBoardWorkSpaceOwnerPermission(IsBoardWorkSpaceOwner):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.board)


class IsPollBoardAdminPermission(IsBoardAdmin):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.board)


class IsPollBoardMemberPermission(IsBoardMember):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.board)


class IsPollAnswerWorkSpaceOwnerPermission(IsPollBoardWorkSpaceOwnerPermission):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.poll)


class IsPollAnswerBoardAdminPermission(IsPollBoardAdminPermission):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.poll)


class IsPollAnswerBoardMemberPermission(IsPollBoardMemberPermission):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.poll)