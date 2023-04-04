from .calendarpermissions import *


class IsEventBoardAdmin(IsCalendarBoardAdmin):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.calendar)


class IsEventBoardMember(IsCalendarBoardMember):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.calendar)


class IsEventBoardWorkSpaceOwner(IsCalendarBoardWorkSpaceOwner):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.calendar)