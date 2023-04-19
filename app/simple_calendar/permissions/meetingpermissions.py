from simple_calendar.permissions.calendarpermissions import *


class IsMeetingBoardAdmin(IsCalendarBoardAdmin):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.calendar)


class IsMeetingBoardMember(IsCalendarBoardMember):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.calendar)


class IsMeetingBoardWorkSpaceOwner(IsCalendarBoardWorkSpaceOwner):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.calendar)