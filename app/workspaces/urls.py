from rest_framework.routers import DefaultRouter
from .views import workspace, chart

router = DefaultRouter()

router.register('workspaces', workspace.WorkspaceViewSet, basename='workspaces')
router.register('workspaces', workspace.WorkSpaceStarredBoardsViewSet, basename='workspaces')
router.register('workspaceowner', workspace.WorkSpaceOwnerViewSet, basename='workspaceowner')
router.register('workspacemember', workspace.WorkSpaceMemberViewSet, basename='workspacemember')
router.register('dashboard', workspace.UserDashboardViewset, basename='dashboard')

router.register('chart', chart.ChartViewSet, basename='chart')


urlpatterns = router.urls