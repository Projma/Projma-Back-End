from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register('workspaces', views.WorkspaceViewSet, basename='workspaces')
router.register('board', views.BoardMembersViewSet, basename='board')
router.register('board', views.BoardInviteLinkViewSet, basename='board')
router.register('board', views.JoinToBoardViewSet, basename='board')
router.register('boardsadminapi', views.BoardAdminViewSet, basename='boardsadminapi')
router.register('boardsmemberapi', views.BoardMembershipViewSet, basename='boardsmemberapi')
router.register('dashboard', views.UserDashboardViewset, basename='dashboard')
router.register('workspaceowner', views.WorkSpaceOwnerViewSet, basename='workspaceowner')
router.register('workspacemember', views.WorkSpaceMemberViewSet, basename='workspacemember')
router.register('board', views.CreateLabelViewSet, basename='board')
router.register('label', views.UpdateLabelViewSet, basename='board')
router.register('label', views.DeleteLabelViewSet, basename='board')
router.register('board', views.GetBoardLabelsViewSet, basename='board')
router.register('tasklist', views.UpdateTaskListViewSet, basename='board')
router.register('board', views.CreateTaskListViewSet, basename='board')
router.register('tasklist', views.DeleteTaskListViewSet, basename='board')
router.register('board', views.GetBoardTaskListsViewSet, basename='board')
router.register('board', views.ReorderTaskListsViewSet, basename='board')


urlpatterns = router.urls