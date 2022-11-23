from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register('workspaces', views.WorkspaceViewSet, basename='workspaces')
router.register(r'workspaces/(?P<w_id>[^/.]+)/boards', views.BoardManagementViewSet, basename='boards')
router.register('dashboard', views.UserDashboardViewset, basename='dashboard')
router.register('workspaceowner', views.WorkSpaceOwnerViewSet, basename='workspaceowner')

urlpatterns = router.urls