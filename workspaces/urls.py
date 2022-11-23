from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register('workspaces', views.WorkspaceViewSet, basename='workspaces')
router.register(r'(?P<w_id>[^/.]+)/boardsadmin', views.BoardAdminViewSet, basename='boardsadmin')
router.register(r'(?P<w_id>[^/.]+)/boardsmember', views.BoardMembershipViewSet, basename='boardsmember')
router.register('dashboard', views.UserDashboardViewset, basename='dashboard')
router.register('workspaceowner', views.WorkSpaceOwnerViewSet, basename='workspaceowner')

urlpatterns = router.urls