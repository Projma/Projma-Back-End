from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import EmailValidator
from django.forms import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from .serializers import *
from .filters import *
from .models import *
from .Email import *
from .permissions import *

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    _ACTIVE_ACCOUNT_KEY = 'active'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        pk = serializer.instance.pk
        self.verify_email(request, pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def verify_email(self, request, pk):
        try:
            user = self.queryset.get(pk=pk)
        except:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        # url = request.get_host() + f'/accounts/users/{self._ACTIVE_ACCOUNT_KEY}'
        url = f'http://{settings.FRONTEND_SOCK}/email-verification'
        email_template = 'emails/bootstrap_email_ev.html'
        context = {'username': user.username}
        email_sender = SendEmail(self.queryset)
        return email_sender.send_email(url, email_template, pk, context)

    @action(detail=False, permission_classes=[AllowAny], methods=['get'])
    def active(self, request, pk=None):
        user_id = request.query_params.get('user_id', '')
        confirmation_token = request.query_params.get('confirmation_token', '')
        try:
            user = self.queryset.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is None:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if not default_token_generator.check_token(user, confirmation_token):
            return Response({'message': 'Invalid or expired token. Please request another confirmation email by signing in.'}, status=status.HTTP_400_BAD_REQUEST)
        if user.is_active:
            return Response({'message': 'User already activated'}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        return Response({'message': 'User activated successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def myaccount(self, request):
        serializer = UserSerializer(instance=request.user)
        try:
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

class ForgotPasswordViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ForgotPasswordSerializer

    def forgot_password(self, request):
        validate_email = EmailValidator()
        email = request.data.get('email')
        try:
            validate_email.__call__(email)
        except ValidationError as e:
            return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = self.queryset.get(email=email)
        except User.DoesNotExist:
            return Response("There is not any user with the given email" , status=status.HTTP_404_NOT_FOUND)
        # url = request.get_host() + f'/accounts/reset-password'
        url = f'http://{settings.FRONTEND_SOCK}/reset-password'
        email_template = 'emails/bootstrap_email_fp.html'
        context = {}
        email_sender = SendEmail(self.queryset)
        return email_sender.send_email(url, email_template, user.pk, context)


class ResetPasswordViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer

    def reset_password(self, request):
        user_id = request.query_params.get('user_id')
        confirmation_token = request.query_params.get('confirmation_token')
        try:
            user = self.queryset.get(pk=user_id)
        except:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        new_password = request.data.get('password')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if user.check_password(new_password):
            return Response('Insert a new password', status=status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(user, confirmation_token):
            return Response({'message': 'Invalid or expired token. Please request another forget password request.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response('Password changed successfully', status=status.HTTP_200_OK)


class ProfileViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    related_search_fields = ['user']
    search_fields = ['user__username', 'user__email']

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def myprofile(self, request):
        serializer = ProfileSerializer(instance=request.user.profile)
        try:
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated], url_path='change-password', serializer_class=ChangePasswordSerializer)
    def change_password(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not user.check_password(old_password):
            return Response({'message': 'Your old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='public-profile/(?P<username>[^/.]+)', serializer_class=PublicInfoProfileSerializer)
    def public_profile(self, request, username):
        profile = get_object_or_404(self.queryset, user__username=username)
        serializer = PublicInfoProfileSerializer(instance=profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EditProfileViewSet(viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = EditProfileSerializer
    permission_classes = [IsAdminUser | IsAuthenticated]
    @action(detail=False, methods=['patch'], url_path='edit-myprofile')
    def edit_myprofile(self, request):
        prof = request.user.profile
        serializer = self.get_serializer(instance=prof,data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteProfilePicViewSet(viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser | IsAuthenticated]
    @action(detail=False, methods=['patch'], url_path='delete-myprofile-pic')
    def delete_myprofile_pic(self, request):
        prof = request.user.profile
        prof.profile_pic = None
        prof.save()
        return Response(self.get_serializer(instance=prof).data, status=status.HTTP_200_OK)