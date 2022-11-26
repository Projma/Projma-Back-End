from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register('workspaces', views.WorkspaceViewSet, basename='workspaces')
router.register('board', views.BoardViewSet, basename='board')
router.register('boardsadmin', views.BoardAdminViewSet, basename='boardsadmin')
router.register('boardsmember', views.BoardMembershipViewSet, basename='boardsmember')
router.register('dashboard', views.UserDashboardViewset, basename='dashboard')
router.register('workspaceowner', views.WorkSpaceOwnerViewSet, basename='workspaceowner')
router.register('workspacemember', views.WorkSpaceMemberViewSet, basename='workspacemember')

urlpatterns = router.urls