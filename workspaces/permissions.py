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
        if request.user.is_superuser or request.user.is_staff:
            return True
        elif obj.owner.user == request.user:
            return True
        return False


class IsBoardAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True
        elif obj.admins.filter(user=request.user.profile).exists() or \
            obj.workspace.owner.user == request.user:
            return True
        return False


class IsMemberOfBoard(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True
        elif obj.members.filter(user=request.user.profile).exists() or \
            obj.workspace.owner.user == request.user:
            return True
        return False