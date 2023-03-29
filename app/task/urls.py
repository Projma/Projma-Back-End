from rest_framework.routers import DefaultRouter
from task.views.task import *
from task.views.checklist import *
from task.views.comment import *

router = DefaultRouter()

router.register('tasklist', CreateTaskViewSet, basename='tasklist')
router.register('tasklist', ReorderTasksViewSet, basename='board')
router.register('task/(?P<b_id>[^/.]+)', FilterBoardViewSet, basename='board')
router.register('task', UpdateTaskViewSet, basename='task')
router.register('task', MoveTaskViewSet, basename='task')
router.register('task', AddLabelsToTaskViewSet, basename='task')
router.register('task', DeleteLabelsFromTaskViewSet, basename='task')
router.register('task', AddDoersToTaskViewSet, basename='task')
router.register('task', DeleteDoersFromTaskViewSet, basename='task')
router.register('task', GetTaskViewSet, basename='task')
router.register('task', GetTaskPreviewViewSet, basename='task')
router.register('task', DeleteTaskViewSet, basename='task')
router.register('task', AddAttachmentToTaskViewSet, basename='task')
router.register('attachment', DeleteAttachmentFromTaskViewSet, basename='attachment')

router.register('task', CreateOrReadCheckListViewSet, basename='checklist')
router.register('task/update-checklist', UpdateCheckListViewSet, basename='checklist')
router.register('task/delete-checklist', DeleteCheckListViewSet, basename='checklist')
router.register('task', NewCommentViewset, basename='task')
router.register('comment', ReplyCommentViewSet, basename='comment')
router.register('comment', EditCommentViewSet, basename='comment')
router.register('comment', DeleteCommentViewSet, basename='comment')