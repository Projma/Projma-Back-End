from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register('', views.WorkSpaceViewSet, basename='workspaces')
router.register(r'(?P<w_id>[^/.]+)/boards', views.BoardViewSet, basename='boards')
router.register('dashboard', views.UserDashboardViewset, basename='dashboard')

urlpatterns = router.urls