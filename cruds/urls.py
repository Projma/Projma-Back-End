from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.CRUDUserViewSet, basename='users')
router.register('profiles', views.CRUDProfileViewSet, basename='profiles')
router.register('workspaces', views.CRUDWorkSpaceViewSet, basename='workspaces')
router.register('boards', views.CRUDBoardViewSet, basename='boards')
router.register('labels', views.CRUDBoardViewSet, basename='labels')

urlpatterns = router.urls