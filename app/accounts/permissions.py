from rest_framework import permissions

class IsProfileUser(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user