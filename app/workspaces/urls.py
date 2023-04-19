from rest_framework.routers import DefaultRouter
from .views import workspace

router = DefaultRouter()

router.register('', workspace.WorkspaceViewSet, basename='workspaces')
router.register('', workspace.WorkSpaceStarredBoardsViewSet, basename='workspaces')
router.register('workspaceowner', workspace.WorkSpaceOwnerViewSet, basename='workspaceowner')
router.register('workspacemember', workspace.WorkSpaceMemberViewSet, basename='workspacemember')
router.register('dashboard', workspace.UserDashboardViewset, basename='dashboard')



urlpatterns = router.urls