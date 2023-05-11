from rest_framework.routers import DefaultRouter
from retro.views import session

router = DefaultRouter()

router.register('', session.SessionViewSet, basename='retro-session')

urlpatterns = router.urls
