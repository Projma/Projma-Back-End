from rest_framework.routers import DefaultRouter
from .views import simplecalendar, event

router = DefaultRouter()

router.register('simple-calendar', simplecalendar.SimpleCalendarViewSet, basename='calendar')
router.register('event', event.EventViewSet, basename='event')

urlpatterns = router.urls