from rest_framework.routers import DefaultRouter
from board.views.board import *

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

urlpatterns = router.urls