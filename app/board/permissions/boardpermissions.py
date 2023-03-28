from rest_framework.permissions import BasePermission, SAFE_METHODS
from workspaces.permissions.workspacepermissions import *

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
