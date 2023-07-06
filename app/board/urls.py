from rest_framework.routers import DefaultRouter
from board.views.board import *
from board.views.label import *
from board.views.tasklist import *
from board.views.poll import *
from board.views.chart import *

router = DefaultRouter()

router.register('(?P<b_id>[^/.]+)/members', BoardMembersViewSet, basename='board')
router.register('(?P<b_id>[^/.]+)', BoardRoleViewSet, basename='board')
router.register('', BoardInviteLinkViewSet, basename='board')
router.register('', RemoveOrJoinToBoardViewSet, basename='board')
router.register('', GetBoardLabelsViewSet, basename='board')
router.register('', GetBoardTaskListsViewSet, basename='board')
router.register('', GetBoardOverviewViewSet, basename='board')
router.register('', ToggleBoardStarViewSet, basename='board')
router.register('boardsadminapi', BoardAdminViewSet, basename='boardsadminapi')
router.register('boardsmemberapi', BoardMembershipViewSet, basename='boardsmemberapi')
router.register('tasklist', CreateTaskListViewSet, basename='board')
router.register('tasklist', ReorderTaskListsViewSet, basename='board')
router.register('tasklist', UpdateTaskListViewSet, basename='board')
router.register('tasklist', DeleteTaskListViewSet, basename='board')
router.register('label', CreateLabelViewSet, basename='board')
router.register('label', UpdateLabelViewSet, basename='board')
router.register('label', DeleteLabelViewSet, basename='board')

router.register('poll', PollViewSet, basename='poll')
router.register('poll-answers', PollAnswerViewSet, basename='poll-answers')

router.register('chart', ChartViewSet, basename='chart')


urlpatterns = router.urls