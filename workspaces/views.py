from rest_framework import viewsets
from rest_framework.response import Response
from .models import WorkSpace
from .serializers import WorkspaceSerializer
from .permissions import WorkSpacePermissions
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