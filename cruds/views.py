from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from .models import *
from .serializers import *


class CRUDUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CRUDUserSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['get', 'patch'])
    def myaccount(self, request):
        if request.method == 'GET':
            serializer = CRUDUserSerializer(instance=request.user)
            try:
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'PATCH':
            instance = request.user
            serializer = CRUDUserSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CRUDProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = CRUDProfileSerializer

    @action(detail=False, methods=['get', 'patch'])
    def myprofile(self, request):
        if request.method == 'GET':
            serializer = CRUDProfileSerializer(instance=request.user.profile)
            try:
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'PATCH':
            instance = request.user.profile
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CRUDWorkSpaceViewSet(viewsets.ModelViewSet):
    queryset = WorkSpace.objects.all()
    serializer_class = CRUDWorkspaceSerializer
    permission_classes = [IsAdminUser]


class CRUDBoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = CRUDBoardSerializer
    permission_classes = [IsAdminUser]

class CRUDLabelViewset(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = CRUDLabelSerializer
    permission_classes = [IsAdminUser]