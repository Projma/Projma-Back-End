from rest_framework.routers import DefaultRouter
from board.views.board import *
from board.views.tasklist import *
from board.views.label import *

router = DefaultRouter()

router.register('board/(?P<b_id>[^/.]+)/members', BoardMembersViewSet, basename='board')
router.register('board/(?P<b_id>[^/.]+)', BoardRoleViewSet, basename='board')
router.register('board', BoardInviteLinkViewSet, basename='board')
router.register('board', RemoveOrJoinToBoardViewSet, basename='board')
router.register('board', GetBoardLabelsViewSet, basename='board')
router.register('board', GetBoardTaskListsViewSet, basename='board')
router.register('board', GetBoardOverviewViewSet, basename='board')
router.register('board', ToggleBoardStarViewSet, basename='board')
router.register('boardsadminapi', BoardAdminViewSet, basename='boardsadminapi')
router.register('boardsmemberapi', BoardMembershipViewSet, basename='boardsmemberapi')
router.register('board', CreateTaskListViewSet, basename='board')
router.register('board', ReorderTaskListsViewSet, basename='board')
router.register('tasklist', UpdateTaskListViewSet, basename='board')
router.register('tasklist', DeleteTaskListViewSet, basename='board')
router.register('board', CreateLabelViewSet, basename='board')
router.register('label', UpdateLabelViewSet, basename='board')
router.register('label', DeleteLabelViewSet, basename='board')

urlpatterns = router.urls