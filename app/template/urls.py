from rest_framework.routers import DefaultRouter
from template.views.template import *

router = DefaultRouter()


router.register('', TemplateViewSet, basename='templates')
router.register('', CreateBoardFromTemplateViewSet, basename='templates')

urlpatterns = router.urls