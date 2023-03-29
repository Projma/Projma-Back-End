from rest_framework.routers import DefaultRouter
from .views import workspace, checklist, templates, comment, chart

router = DefaultRouter()

router.register('workspaces', workspace.WorkspaceViewSet, basename='workspaces')
router.register('workspaces', workspace.WorkSpaceStarredBoardsViewSet, basename='workspaces')
router.register('workspaceowner', workspace.WorkSpaceOwnerViewSet, basename='workspaceowner')
router.register('workspacemember', workspace.WorkSpaceMemberViewSet, basename='workspacemember')
router.register('dashboard', workspace.UserDashboardViewset, basename='dashboard')


router.register('task', checklist.CreateOrReadCheckListViewSet, basename='checklist')
router.register('task/update-checklist', checklist.UpdateCheckListViewSet, basename='checklist')
router.register('task/delete-checklist', checklist.DeleteCheckListViewSet, basename='checklist')
router.register('task', comment.NewCommentViewset, basename='task')
router.register('comment', comment.ReplyCommentViewSet, basename='comment')
router.register('comment', comment.EditCommentViewSet, basename='comment')
router.register('comment', comment.DeleteCommentViewSet, basename='comment')

router.register('templates', templates.TemplateViewSet, basename='templates')
router.register('templates', templates.CreateBoardFromTemplateViewSet, basename='templates')
router.register('chart', chart.ChartViewSet, basename='chart')


urlpatterns = router.urls