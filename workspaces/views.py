from rest_framework import viewsets
from .models import WorkSpace
from .serializers import WorkspaceSerializer
# Create your views here.

class WorkSpaceViewSet(viewsets.ModelViewSet):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkspaceSerializer