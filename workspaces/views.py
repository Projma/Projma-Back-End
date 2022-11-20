from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *
from .permissions import *
# Create your views here.

class WorkSpaceViewSet(viewsets.ModelViewSet):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [WorkSpacePermissions]

    def list(self, request, *args, **kwargs):
        user = request.user
        if request.user.is_staff:
            serializer = self.get_serializer(self.get_queryset(), many=True)
        else:
            serializer = self.get_serializer(self.queryset.filter(owner__user=user), many=True)
        return Response(serializer.data)


class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer

    def get_queryset(self):
        path = self.request.path.strip('/').split()
        workspace_id = int(path[1])
        workspace = get_object_or_404(WorkSpace, pk=workspace_id)
        boards = Board.objects.filter(workspace=workspace)
        return boards