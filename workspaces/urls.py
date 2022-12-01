from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register('workspaces', views.WorkspaceViewSet, basename='workspaces')
router.register('board', views.BoardMembersViewSet, basename='board')
router.register('board', views.BoardInviteLinkViewSet, basename='board')
router.register('board', views.BoardJoinViewSet, basename='board')
router.register('boardsadminapi', views.BoardAdminViewSet, basename='boardsadminapi')
router.register('boardsmemberapi', views.BoardMembershipViewSet, basename='boardsmemberapi')
router.register('dashboard', views.UserDashboardViewset, basename='dashboard')
router.register('workspaceownerapi', views.WorkSpaceOwnerViewSet, basename='workspaceownerapi')
router.register('workspacememberapi', views.WorkSpaceMemberViewSet, basename='workspacememberapi')

urlpatterns = router.urls