from rest_framework.routers import DefaultRouter
from task.views.task import *
from task.views.checklist import *
from task.views.comment import *

router = DefaultRouter()

router.register('', CreateTaskViewSet, basename='task')
router.register('', ReorderTasksViewSet, basename='board')
router.register('(?P<b_id>[^/.]+)', FilterBoardViewSet, basename='board')
router.register('', UpdateTaskViewSet, basename='task')
router.register('', MoveTaskViewSet, basename='task')
router.register('', AddLabelsToTaskViewSet, basename='task')
router.register('', DeleteLabelsFromTaskViewSet, basename='task')
router.register('', AddDoersToTaskViewSet, basename='task')
router.register('', DeleteDoersFromTaskViewSet, basename='task')
router.register('', GetTaskViewSet, basename='task')
router.register('', GetTaskPreviewViewSet, basename='task')
router.register('delete-task', DeleteTaskViewSet, basename='task')
router.register('attachment', AddAttachmentToTaskViewSet, basename='task')
router.register('attachment', DeleteAttachmentFromTaskViewSet, basename='attachment')
router.register('checklist', CreateOrReadCheckListViewSet, basename='checklist')
router.register('checklist/update-checklist', UpdateCheckListViewSet, basename='checklist')
router.register('checklist/delete-checklist', DeleteCheckListViewSet, basename='checklist')
router.register('comment', NewCommentViewset, basename='task')
router.register('comment', ReplyCommentViewSet, basename='comment')
router.register('comment', EditCommentViewSet, basename='comment')
router.register('comment', DeleteCommentViewSet, basename='comment')

urlpatterns = router.urls