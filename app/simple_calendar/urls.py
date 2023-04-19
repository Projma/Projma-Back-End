from rest_framework.routers import DefaultRouter
from .views import simplecalendar, event, meeting

router = DefaultRouter()

router.register('simple-calendar', simplecalendar.SimpleCalendarViewSet, basename='calendar')
router.register('event', event.EventViewSet, basename='event')
router.register('meeting', meeting.CreateMeetingViewSet, basename='meeting')
router.register('meeting', meeting.UpdateMeetingViewSet, basename='meeting')
router.register('meeting', meeting.DeleteMeetingViewSet, basename='meeting')
router.register('meeting', meeting.GetCalendarMeetingsViewSet, basename='meeting')
router.register('meeting', meeting.StartMeetingViewSet, basename='meeting')
router.register('meeting', meeting.EndMeetingViewSet, basename='meeting')

urlpatterns = router.urls
