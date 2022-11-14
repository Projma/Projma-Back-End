from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .routers import *
from .models import *
from .views import *

userrouter = UserRouter()
userrouter.register('users', UserViewSet, basename='user')

router = DefaultRouter()
router.register('profile', ProfileViewset, basename='profile')

urlpatterns = userrouter.urls
urlpatterns += router.urls

urlpatterns += [
    path('forgot-password/', ForgotPasswordViewSet.as_view({'post': 'forgot_password'})),
    path('reset-password/', ResetPasswordViewSet.as_view({'post': 'reset_password'})),
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]