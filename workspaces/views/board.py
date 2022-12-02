from django.shortcuts import get_object_or_404 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter
from rest_framework import status
from ..invite_link import encode, decode
from ..models import *
from ..serializers.boardserializers import *
from ..permissions.boardpermissions import *
from accounts.serializers import *


class BoardAdminViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardAdminSerializer
    permission_classes = [IsBoardAdmin | IsAdminUser | IsWorkSpaceOwner]

    @action(detail=True, methods=['patch'], url_path='edit-board')
    def edit_board(self, request, pk):
        board = self.get_object()
        serializer = BoardAdminSerializer(instance=board, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['delete'], url_path='delete-board')
    def delete_board(self, request, pk):
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
    permission_classes = [IsBoardMember | IsAdminUser | IsBoardAdmin | IsWorkSpaceOwner]

    @action(detail=True, methods=['get'], url_path='get-board')
    def get_board(self, request, pk):
        board = self.get_object()
        serializer = BoardMemberSerializer(instance=board)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BoardMembersViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardMemberSerializer
    permission_classes = [IsBoardMember | IsAdminUser | IsBoardAdmin | IsBoardWorkSpaceOwner]
    serializer_class = BoardMembersSerializer
    permission_classes = [IsBoardMember | IsAdminUser | IsBoardAdmin | IsWorkSpaceOwner]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    related_search_fields = ['user']
    search_fields = ['user__username', 'user__email']

    def get_queryset(self):
        board_id = self.kwargs['b_id']
        board = get_object_or_404(Board, pk=board_id)
        owner = Profile.objects.filter(user=board.workspace.owner).all()
        qs = board.members.all() | board.admins.all() | owner
        return qs

    def list(self, request, *args, **kwargs):
        pk = kwargs.get('b_id')
        qs = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(instance=qs, many=True, context={'board': pk})
        return Response(serializer.data, status=status.HTTP_200_OK)


class BoardInviteLinkViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardAdminSerializer
    permission_classes = [IsBoardAdmin | IsAdminUser | IsWorkSpaceOwner]

    @action(detail=True, methods=['get'], url_path='')
    def invite_link(self, request, pk):
        board = self.get_object()
        invite_link = encode(board)
        return Response(invite_link, status=status.HTTP_200_OK)


class JoinToBoardViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardMemberSerializer
    permission_classes = [IsAuthenticated]

    def add_to_board(self, board, user):
        if board is None:
            return Response('Invalid invite link', status=status.HTTP_400_BAD_REQUEST)
        try:
            qs = board.members.all() | board.admins.all()
            if user.profile in qs or user.profile == board.workspace.owner:
                return Response('You are already a member of this board', status=status.HTTP_400_BAD_REQUEST)
            board.members.add(user.profile)
            return Response('You have been added to the board successfully', status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f'{repr(e)}', status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='join-to-board/(?P<invite_link>.+)', permission_classes=[IsAuthenticated])
    def join_board(self, request, invite_link):
        board = decode(invite_link)
        return self.add_to_board(board, request.user)

    @action(detail=True, methods=['post'], url_path='add-user-to-board/(?P<user_id>.+)', permission_classes=[IsBoardAdmin | IsAdminUser | IsWorkSpaceOwner])
    def add_user_to_board(self, request, pk, user_id):
        board = self.get_object()
        user = get_object_or_404(User, pk=user_id)
        return self.add_to_board(board, user)


class GetBoardLabelsViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsAdminUser | IsBoardMember | IsBoardAdmin | IsBoardWorkSpaceOwner]
    @action(detail=True, methods=['get'])
    def get_board_labels(self, request, pk):
        board = self.get_object()
        serializer = self.get_serializer(instance = Label.objects.all().filter(board=board), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetBoardTaskListsViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsBoardMember | IsAdminUser | IsBoardAdmin | IsBoardWorkSpaceOwner]
    @action(detail=True, methods=['get'])
    def get_board_labels(self, request, pk):
        board = self.get_object()
        serializer = self.get_serializer(instance = TaskList.objects.all().filter(board=board), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
