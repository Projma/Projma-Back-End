from rest_framework.permissions import BasePermission, SAFE_METHODS


class WorkSpacePermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return bool(request.user and request.user.is_authenticated)
        elif request.method == 'GET':
            return bool(request.user and request.user.is_staff)
        return True

    # def has_object_permission(self, request, view, obj):
    #     if request.user.is_superuser or request.user.is_staff:
    #         return True
    #     elif obj.owner.user == request.user:
    #         return True
    #     return False