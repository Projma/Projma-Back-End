from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from .serializers import *
from .models import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminUser()]
        return [AllowAny()]
