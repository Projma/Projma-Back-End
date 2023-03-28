from rest_framework.routers import DefaultRouter
from tasklist.views.tasklist import *

router = DefaultRouter()

router.register('board', CreateTaskListViewSet, basename='board')
router.register('board', ReorderTaskListsViewSet, basename='board')
router.register('tasklist', UpdateTaskListViewSet, basename='board')
router.register('tasklist', DeleteTaskListViewSet, basename='board')

urlpatterns = router.urls