from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .routers import *
from .models import *
from .views import *

router = UserRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = router.urls

urlpatterns += [
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]