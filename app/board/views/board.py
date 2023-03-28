from django.shortcuts import get_object_or_404 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter
from rest_framework import status
from workspaces.invite_link import encode, decode
from ..models import *
from board.permissions.boardpermissions import *
from accounts.serializers import *
from board.serializers.boardserializers import *
from board.models import Board


class BoardAdminViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardAdminSerializer
    permission_classes = [IsBoardAdmin | IsAdminUser | IsBoardWorkSpaceOwner]

    @action(detail=True, methods=['patch'], url_path='edit-board')
    def edit_board(self, request, pk):
        board = self.get_object()
        serializer = BoardAdminSerializer(instance=board, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='delete-board')
    def delete_board(self, request, pk):
        board = get_object_or_404(Board, pk=pk)
        if board.workspace:
            board = self.get_object()
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='get-board')
    def get_board(self, request, pk):
        board = self.get_object()
        serializer = BoardAdminSerializer(instance=board)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BoardMembershipViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardMemberSerializer
    permission_classes = [IsBoardMember | IsAdminUser | IsBoardAdmin | IsBoardWorkSpaceOwner]

    @action(detail=True, methods=['get'], url_path='get-board')
    def get_board(self, request, pk):
        board = self.get_object()
        serializer = BoardMemberSerializer(instance=board)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BoardMembersViewSet(viewsets.GenericViewSet):
    serializer_class = BoardMembersSerializer
    permission_classes = [IsBoardMember | IsAdminUser | IsBoardAdmin | IsBoardWorkSpaceOwner]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    related_search_fields = ['user']
    search_fields = ['user__username', 'user__email']

    def get_queryset(self):
        board_id = self.kwargs['b_id']
        board = get_object_or_404(Board, pk=board_id)
        self.check_object_permissions(self.request, board)
        owner = Profile.objects.filter(user=board.workspace.owner).all()
        qs = board.members.all() | board.admins.all() | owner
        return qs.distinct()

    def list(self, request, *args, **kwargs):
        pk = kwargs.get('b_id')
        qs = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(instance=qs, many=True, context={'board': pk})
        return Response(serializer.data, status=status.HTTP_200_OK)


class BoardRoleViewSet(viewsets.GenericViewSet):
    serializer_class = BoardChangeRoleSerializer
    permission_classes = [IsBoardAdmin | IsAdminUser | IsBoardWorkSpaceOwner]

    def get_queryset(self):
        board_id = self.kwargs['b_id']
        board = get_object_or_404(Board, pk=board_id)
        owner = Profile.objects.filter(user=board.workspace.owner).all()
        qs = board.members.all() | board.admins.all() | owner
        return qs.distinct()

    @action(detail=False, methods=['put'], url_path='change-role')
    def change_role(self, request, *args, **kwargs):
        board_id = kwargs.get('b_id')
        board = get_object_or_404(Board, pk=board_id)
        self.check_object_permissions(request, board)
        user_id = request.data.get('user_id')
        user = get_object_or_404(Profile, pk=user_id)
        if not user in self.get_queryset():
            return Response({'error': 'User is not a member of this board'}, status=status.HTTP_400_BAD_REQUEST)
        role = request.data.get('role')
        serializer = BoardChangeRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if user == board.workspace.owner:
            return Response({'detail': 'User is the owner of the workspace of the board. Owner can not be changed'}, status=status.HTTP_400_BAD_REQUEST)
        if role == 'Admin':
            if user in board.members.all():
                board.members.remove(user)
            if not user in board.admins.all():
                board.admins.add(user)
        elif role == 'Member':
            if user in board.admins.all():
                board.admins.remove(user)
            if not user in board.members.all():
                board.members.add(user)
        board.save()
        return Response('Role changed successfully', status=status.HTTP_200_OK)


class BoardInviteLinkViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardAdminSerializer
    permission_classes = [IsBoardAdmin | IsAdminUser | IsBoardWorkSpaceOwner]

    @action(detail=True, methods=['get'], url_path='')
    def invite_link(self, request, pk):
        board = self.get_object()
        invite_link = encode(board)
        return Response(invite_link, status=status.HTTP_200_OK)


class RemoveOrJoinToBoardViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardMembersSerializer
    permission_classes = [IsAuthenticated]

    def add_to_board(self, board, user):
        if board is None:
            return Response('Invalid invite link', status=status.HTTP_400_BAD_REQUEST)
        try:
            # qs = board.members.all() | board.admins.all()
            qs = board.members.all()
            # if user.profile in qs or user.profile == board.workspace.owner:
            if user.profile in qs:
                return Response('User is already a member of this board', status=status.HTTP_400_BAD_REQUEST)
            board.members.add(user.profile)
            return Response('User added to the board successfully', status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f'{repr(e)}', status=status.HTTP_400_BAD_REQUEST)

    def remove_from_board(self, board, user):
        if board is None:
            return Response('Invalid invite link', status=status.HTTP_400_BAD_REQUEST)
        try:
            qs = board.members.all() | board.admins.all()
            if user.profile == board.workspace.owner:
                return Response('User is the owner of the workspace of the board. Owner can not be removed', status=status.HTTP_400_BAD_REQUEST)
            elif user.profile not in qs:
                return Response('User is not a member of this board', status=status.HTTP_400_BAD_REQUEST)
            if user.profile in board.admins.all():
                board.admins.remove(user.profile)
            elif user.profile in board.members.all():
                board.members.remove(user.profile)
            board.save()
            return Response('User removed successfully', status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f'{repr(e)}', status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='join-to-board/(?P<invite_link>.+)', permission_classes=[IsAuthenticated])
    def join_board(self, request, invite_link):
        try:
            board = decode(invite_link)
        except:
            board = None
        return self.add_to_board(board, request.user)

    @action(detail=True, methods=['post'], url_path='add-user-to-board/(?P<user_id>.+)', permission_classes=[IsBoardAdmin | IsAdminUser | IsBoardWorkSpaceOwner])
    def add_user_to_board(self, request, pk, user_id):
        board = self.get_object()
        self.check_object_permissions(request, board)
        user = get_object_or_404(User, pk=user_id)
        return self.add_to_board(board, user)

    @action(detail=True, methods=['delete'], url_path='remove-user-from-board/(?P<user_id>.+)', permission_classes=[IsBoardAdmin | IsAdminUser | IsBoardWorkSpaceOwner])
    def remove_user_from_board(self, request, pk, user_id):
        board = self.get_object()
        user = get_object_or_404(User, pk=user_id)
        return self.remove_from_board(board, user)


class GetBoardLabelsViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsAdminUser | IsBoardMember | IsBoardAdmin | IsBoardWorkSpaceOwner]
    @action(detail=True, methods=['get'],url_path='get-board-labels')
    def get_board_labels(self, request, pk):
        board = self.get_object()
        serializer = self.get_serializer(instance = Label.objects.all().filter(board=board), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetBoardTaskListsViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsBoardMember | IsAdminUser | IsBoardAdmin | IsBoardWorkSpaceOwner]
    @action(detail=True, methods=['get'], url_path='get-board-tasklists')
    def get_board_tasklists(self, request, pk):
        board = self.get_object()
        serializer = self.get_serializer(instance = TaskList.objects.all().filter(board=board), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetBoardOverviewViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardOverviewSerializer
    permission_classes = [IsAdminUser | IsBoardMember | IsBoardAdmin | IsBoardWorkSpaceOwner]
    @action(detail=True, methods=['get'], url_path='get-board-overview')
    def get_board_overview(self, request, pk):
        board = self.get_object()
        LogUserRecentBoards.set_lastseen(profile=request.user.profile, board=board)
        serializer = self.get_serializer(instance=board)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ToggleBoardStarViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardIdsSerializer
    permission_classes = [IsAdminUser | IsBoardMember | IsBoardAdmin | IsBoardWorkSpaceOwner]

    @action(detail=True, methods=['post'], url_path='toggle-myboard-star')
    def toggle_board_star(self, request, pk):
        board = self.get_object()
        user = request.user
        if board in user.profile.starred_boards.all():
            user.profile.starred_boards.remove(board)
        else:
            user.profile.starred_boards.add(board)
        serializer = self.get_serializer(
            instance={'board_ids': user.profile.starred_boards.all().values_list('id', flat=True)})
        return Response(serializer.data, status=status.HTTP_200_OK)