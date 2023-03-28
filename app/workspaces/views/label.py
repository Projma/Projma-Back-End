from django.shortcuts import get_object_or_404 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from ..models import *
from ..serializers.labelserializers import *
from ..permissions.labelpermissions import *
from accounts.serializers import *
from board.models import Board


class CreateLabelViewSet(viewsets.GenericViewSet):
    queryset = Board.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsBoardMember | IsAdminUser | IsBoardAdmin | IsBoardWorkSpaceOwner]
    @action(detail=True, methods=['post'], url_path='create-label')
    def create_label(self, request, pk):
        board = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(board=board)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateLabelViewSet(viewsets.GenericViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsAdminUser | IsLabelBoardAdmin | IsLabelBoardMember | IsLabelBoardWorkSpaceOwner]
    @action(detail=True, methods=['patch'], url_path='update-label')
    def update_label(self, request, pk):
        label = self.get_object()
        serializer = self.get_serializer(instance=label, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteLabelViewSet(viewsets.GenericViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsAdminUser | IsLabelBoardAdmin | IsLabelBoardMember | IsLabelBoardWorkSpaceOwner]
    @action(detail=True, methods=['delete'], url_path='delete-label')
    def delete_label(self, request, pk):
        label = self.get_object()
        label.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
