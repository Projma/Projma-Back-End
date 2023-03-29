from rest_framework.routers import DefaultRouter
from template.views.template import *

router = DefaultRouter()


router.register('templates', TemplateViewSet, basename='templates')
router.register('templates', CreateBoardFromTemplateViewSet, basename='templates')

urlpatterns = router.urls