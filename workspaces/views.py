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

class WorkspaceViewSet(viewsets.GenericViewSet):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkspaceSerializer

    @action(methods=['get'], detail=False)
    def type(self, request):
        types = WorkSpace.TYPE_CHOICES
        dic_types = {t[0]: t[1] for t in types}
        return Response(dic_types)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated], url_path='join-to-workspace/(?P<invite_link>.+)')
    def join_to_workspace(self, request, invite_link):
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
        return {'workspace_id': workspace_id, 'request': self.request}


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAdminUser]


class UserDashboardViewset(viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=False, url_path='create-workspace')
    def create_workspace(self, request):
        serializer = WorkspaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user.profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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

    @action(detail=True, methods=['patch'], url_path='edit-workspace')
    def edit_workspace(self, request, pk):
        workspace = self.get_object()
        serializer = WorkspaceSerializer(instance=workspace, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='get-workspace')
    def get_workspace(self, request, pk):
        workspace = self.get_object()
        serializer = WorkspaceSerializer(instance=workspace)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='delete-workspace')
    def delete_workspace(self, request, pk):
        workspace = self.get_object()
        workspace.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True, permission_classes=[IsWorkSpaceOwner]) 
    def invite_link(self, request, pk):
        workspace = self.get_object()
        invite_link = encode(workspace)
        return Response(invite_link, status=status.HTTP_200_OK)