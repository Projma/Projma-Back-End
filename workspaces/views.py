from django.shortcuts import get_object_or_404 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .invite_link import encode, decode
from .models import *
from .serializers import *
from .permissions import *
from accounts.serializers import *
# Create your views here.

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        if request.user.is_staff:
            serializer = self.get_serializer(self.get_queryset(), many=True)
        else:
            serializer = self.get_serializer(self.queryset.filter(owner__user=user), many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def type(self, request):
        types = WorkSpace.TYPE_CHOICES
        dic_types = {t[0]: t[1] for t in types}
        return Response(dic_types)

    @action(methods=['get'], detail=True)
    def invite_link(self, request, pk):
        workspace = self.get_object()
        if workspace.owner.user == request.user:
            invite_link = encode(workspace)
            return Response(invite_link)
        else:
            return Response('You are not authorized to view this link', status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['get'], detail=False, url_path='invite-to-workspace/(?P<invite_link>.+)')
    def invite_to_workspace(self, request, invite_link):
        workspace = decode(invite_link)
        if workspace is None:
            return Response('Invalid invite link', status=status.HTTP_400_BAD_REQUEST)
        try:
            if request.user.profile in workspace.members.all():
                return Response('You are already a member of this workspace', status=status.HTTP_400_BAD_REQUEST)
            workspace.members.add(request.user.profile)
            return Response('You have been added to the workspace successfully', status=status.HTTP_200_OK)
        except:
            return Response('Adding user to workspace failed', status=status.HTTP_400_BAD_REQUEST)


class BoardManagementViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer

    def get_queryset(self):
        workspace_id = self.kwargs.get('w_id')
        if workspace_id is not None:
            workspace = get_object_or_404(WorkSpace, pk=workspace_id)
            boards = Board.objects.filter(workspace=workspace)
        else:
            boards = Board.objects.all()
        return boards

    def get_serializer_context(self):
        workspace_id = self.kwargs.get('w_id')
        return {'workspace_id': workspace_id}


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAdminUser]


class UserDashboardViewset(viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def myboards(self, request):
        serializer = BoardSerializer(instance=list(request.user.profile.boards.all()), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)        
    
    @action(detail=False, methods=['get'])
    def myadministrating_boards(self, request):
        serializer = BoardSerializer(instance=list(request.user.profile.administrating_boards.all()), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
            
    @action(detail=False, methods=['get'])
    def myworkspaces(self, request):
        serializer = WorkspaceSerializer(instance=list(request.user.profile.workspaces.all()), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def myowning_workspaces(self, request):
        serializer = WorkspaceSerializer(instance=list(request.user.profile.owning_workspaces.all()), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkSpaceOwnerViewSet(viewsets.GenericViewSet):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [IsWorkSpaceOwner]
    @action(detail=True, methods=['get'], url_path='memberboards/(?P<memberid>\d+)')
    def memberboards(self, request, pk, memberid):
        memberprofile = get_object_or_404(Profile, pk=memberid)
        serializer = BoardSerializer(instance=memberprofile.boards.all().filter(workspace=pk), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
