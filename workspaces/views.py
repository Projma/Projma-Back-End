from rest_framework import viewsets
from .models import WorkSpace
from .serializers import WorkspaceSerializer
from .permissions import WorkSpacePermissions
# Create your views here.

class WorkSpaceViewSet(viewsets.ModelViewSet):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [WorkSpacePermissions]