from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register('', views.WorkSpaceViewSet, basename='workspaces')
router.register(r'\d'+'/boards', views.BoardViewSet, basename='boards')

urlpatterns = router.urls