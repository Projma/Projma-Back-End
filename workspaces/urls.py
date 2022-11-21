from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register('workspaces', views.WorkSpaceViewSet, basename='workspaces')
router.register(r'workspaces/(?P<w_id>[^/.]+)/boards', views.BoardManagementViewSet, basename='boards')
router.register('boards', views.BoardViewSet, basename='boards')
router.register('dashboard', views.UserDashboardViewset, basename='dashboard')

urlpatterns = router.urls