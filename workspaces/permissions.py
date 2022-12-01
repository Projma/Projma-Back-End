from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Board, WorkSpace, Profile


class WorkSpacePermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        if not request.user or request.user.is_anonymous:
            return False
        if request.method == 'POST' or request.method == 'DELETE':
            return bool(request.user and request.user.is_authenticated)
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True
        elif obj.owner.user == request.user:
            return True
        return False


class IsWorkSpaceOwner(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if obj.owner.user == request.user:
            return True
        return False


class IsBoardWorkSpaceOwner(IsWorkSpaceOwner):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.workspace)



class IsBoardAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if obj.admins.filter(user=request.user.profile).exists():
            return True
        return False


class IsBoardMember(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if obj.members.filter(user=request.user.profile).exists():
            return True
        return False

class IsWorkSpaceMember(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.profile in obj.members.all():
            return True
        return False

class IsLabelBoardMember(IsBoardMember):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.board)


class IsLabelBoardAdmin(IsBoardAdmin):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.board)


class IsLabelBoardWorkSpaceOwner(IsBoardWorkSpaceOwner):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.board)


class IsTaskListBoardMember(IsBoardMember):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.board)


class IsTaskListBoardAdmin(IsBoardAdmin):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.board)


class IsTaskListBoardWorkSpaceOwner(IsBoardWorkSpaceOwner):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.board)

