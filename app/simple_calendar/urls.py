from rest_framework.routers import DefaultRouter
from .views import simplecalendar

router = DefaultRouter()

router.register('', simplecalendar.SimpleCalendarViewSet, basename='calendar')

urlpatterns = router.urls