from django.urls import include, path
from rest_framework import routers
from .routers import *
from .models import *
from .views import *

router = UserRouter()
router.register('users', UserViewset, basename='user')


urlpatterns = [
    path('', include(router.urls))
]