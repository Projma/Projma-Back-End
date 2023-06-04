from rest_framework.routers import DefaultRouter
from retro.views import session

router = DefaultRouter()

router.register('', session.SessionViewSet, basename='retro-session')
router.register('', session.GetSessionReflect, basename='retro-session')
router.register('', session.GetSessionGroup, basename='retro-session')
router.register('', session.GetSessionVote, basename='retro-session')
router.register('', session.GetSessionDiscuss, basename='retro-session')

urlpatterns = router.urls
