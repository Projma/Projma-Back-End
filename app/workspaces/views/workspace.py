from django.shortcuts import get_object_or_404 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from ..invite_link import encode, decode
# from ..models import *
from workspaces.models import WorkSpace
from board.models import Board, LogUserRecentBoards
from ..serializers.workspaceserializers import *
from board.serializers.boardserializers import *
from ..permissions.workspacepermissions import *
from accounts.serializers import *



class WorkspaceViewSet(viewsets.GenericViewSet):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkSpaceMemberSerializer

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
            qs = workspace.members.all()
            if request.user.profile in qs or request.user.profile == workspace.owner:
                return Response('You are already a member of this workspace', status=status.HTTP_400_BAD_REQUEST)
            workspace.members.add(request.user.profile)
            return Response('You have been added to the workspace successfully', status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f'{repr(e)}', status=status.HTTP_400_BAD_REQUEST)


class UserDashboardViewset(viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = WorkSpaceMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_recent_boards_limit(self):
        return 10

    @action(methods=['post'], detail=False, url_path='create-workspace', serializer_class=WorkSpaceOwnerSerializer)
    def create_workspace(self, request):
        serializer = WorkSpaceOwnerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user.profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], serializer_class=BoardAdminSerializer)
    def myboards(self, request):
        myownworks = request.user.profile.owning_workspaces.all()
        qs = request.user.profile.boards.all() | request.user.profile.administrating_boards.all() \
            | Board.objects.filter(workspace__in=myownworks)
        serializer = BoardMemberSerializer(instance=qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)        
    
    @action(detail=False, methods=['get'], serializer_class=BoardAdminSerializer, url_path='myadministrating-boards')
    def myadministrating_boards(self, request):
        serializer = BoardAdminSerializer(instance=list(request.user.profile.administrating_boards.all()), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], serializer_class=WorkSpaceOwnerSerializer)
    def myworkspaces(self, request):
        qs = request.user.profile.workspaces.all() | request.user.profile.owning_workspaces.all()
        serializer = WorkSpaceMemberSerializer(instance=qs.distinct(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='myowning-workspaces', serializer_class=WorkSpaceOwnerSerializer)
    def myowning_workspaces(self, request):
        serializer = WorkSpaceOwnerSerializer(instance=list(request.user.profile.owning_workspaces.all()), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='mystarred-boards')
    def mystarred_boards(self, request):
        prof = request.user.profile
        serializer = BoardMemberSerializer(instance=prof.starred_boards.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='myrecent-boards')
    def myrecent_boards(self, request):
        prof = request.user.profile
        recentboardids = LogUserRecentBoards.objects. \
            filter(profile=prof).order_by('-lastseen')[:self.get_recent_boards_limit()].values_list('board', flat=True)
        
        recentboards = [Board.objects.get(id=bid) for bid in recentboardids]
        serializer = BoardMemberSerializer(instance=recentboards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkSpaceOwnerViewSet(viewsets.GenericViewSet):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkSpaceOwnerSerializer
    permission_classes = [IsWorkSpaceOwner | IsAdminUser]

    @action(detail=True, methods=['get'], url_path='memberboards/(?P<memberid>\d+)', serializer_class=BoardAdminSerializer)
    def memberboards(self, request, pk, memberid):
        memberprofile = get_object_or_404(Profile, pk=memberid)
        serializer = BoardAdminSerializer(instance=memberprofile.boards.all().filter(workspace=pk), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_path='workspace-members', serializer_class=ProfileSerializer)
    def workspace_members(self, request, pk):
        serializer = ProfileSerializer(instance=self.get_object().members.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='workspace-boards', serializer_class=BoardAdminSerializer)
    def workspace_boards(self, request, pk):
        serializer = BoardAdminSerializer(instance=self.get_object().boards.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='edit-workspace')
    def edit_workspace(self, request, pk):
        workspace = self.get_object()
        serializer = WorkSpaceOwnerSerializer(instance=workspace, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='get-workspace')
    def get_workspace(self, request, pk):
        workspace = self.get_object()
        serializer = WorkSpaceOwnerSerializer(instance=workspace)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='delete-workspace')
    def delete_workspace(self, request, pk):
        workspace = self.get_object()
        workspace.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True, permission_classes=[IsWorkSpaceOwner], url_path='invite-link') 
    def invite_link(self, request, pk):
        workspace = self.get_object()
        invite_link = encode(workspace)
        return Response(invite_link, status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=True, url_path='create-board', serializer_class=BoardAdminSerializer)
    def create_board(self, request, pk):
        ws = self.get_object()
        serializer = BoardAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(workspace=ws)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='add-user-to-workspace/(?P<user_id>.+)', serializer_class=WorkSpaceMemberSerializer)
    def add_user_to_workspace(self, request, pk, user_id):
        workspace = self.get_object()
        self.check_object_permissions(request, workspace)
        user = get_object_or_404(Profile, pk=user_id)
        return self.add_to_workspace(workspace, user)

    @action(methods=['delete'], detail=True, url_path='remove-user-from-workspace/(?P<user_id>.+)', serializer_class=WorkSpaceMemberSerializer)
    def remove_user_from_workspace(self, request, pk, user_id):
        workspace = self.get_object()
        user = get_object_or_404(Profile, pk=user_id)
        return self.remove_from_workspace(workspace, user)

    def add_to_workspace(self, workspace, user):
        if workspace is None:
            return Response('Workspace does not exist', status=status.HTTP_400_BAD_REQUEST)
        try:
            if user in workspace.members.all() or user == workspace.owner:
                return Response('User is already a member of the workspace', status=status.HTTP_400_BAD_REQUEST)
            workspace.members.add(user)
            return Response('User added to workspace successfully', status=status.HTTP_200_OK)
        except Exception as e:
            return Response(repr(e), status=status.HTTP_400_BAD_REQUEST)

    def remove_from_workspace(self, workspace, user):
        if workspace is None:
            return Response('Workspace does not exist', status=status.HTTP_400_BAD_REQUEST)
        try:
            if user == workspace.owner:
                return Response('You cannot remove the owner of the workspace', status=status.HTTP_400_BAD_REQUEST)
            if user not in workspace.members.all():
                return Response('User is not a member of the workspace', status=status.HTTP_400_BAD_REQUEST)
            workspace.members.remove(user)
            workspace.save()
            return Response('User removed from workspace successfully', status=status.HTTP_200_OK)
        except Exception as e:
            return Response(repr(e), status=status.HTTP_400_BAD_REQUEST)

class WorkSpaceMemberViewSet(viewsets.GenericViewSet):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkSpaceMemberSerializer
    permission_classes = [IsWorkSpaceMember | IsAdminUser | IsWorkSpaceOwner]

    @action(detail=True, methods=['get'], url_path='workspace-boards', serializer_class=BoardMemberSerializer)
    def workspace_boards(self, request, pk):
        serializer = BoardMemberSerializer(instance=self.get_object().boards.all().filter(members__user=request.user), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WorkSpaceStarredBoardsViewSet(viewsets.GenericViewSet):
    queryset = WorkSpace.objects.all()
    serializer_class = BoardMemberSerializer
    permission_classes = [IsWorkSpaceMember | IsAdminUser | IsWorkSpaceOwner]

    @action(detail=True, methods=['get'], url_path='workspace-starred-boards', serializer_class=BoardMemberSerializer)
    def workspace_boards(self, request, pk):
        ws = self.get_object()
        userstarredboards = request.user.profile.starred_boards.all().filter(workspace=ws)
        serializer = self.get_serializer(instance=userstarredboards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)