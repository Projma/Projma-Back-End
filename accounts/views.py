from django.contrib.auth.tokens import default_token_generator
from django.core.validators import EmailValidator
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from templated_mail.mail import BaseEmailMessage
from .serializers import *
from .models import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    _ACTIVE_ACCOUNT_KEY = 'active'
    _FORGOT_PASSWORD_KEY = 'forgot_password'
    _RESET_PASSWORD_KEY = 'reset_password'

    def get_permissions(self):
        if self.request.method == 'GET' \
            and not self._FORGOT_PASSWORD_KEY in self.request.path \
            and not self._RESET_PASSWORD_KEY in self.request.path:
                return [IsAdminUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self._FORGOT_PASSWORD_KEY in self.request.path:
            return ForgotPassword
        elif self._RESET_PASSWORD_KEY in self.request.path:
            return ResetPassword
        return CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        pk = serializer.instance.pk
        self.verify_email(request, pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def send_email(self, url, email_template, pk, context):
        try:
            user = self.queryset.get(pk=pk)
            user_email = user.email
            confirmation_token = default_token_generator.make_token(user)
        except:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        try:
            base_url = url
            response_url = f'{base_url}?user_id={user.pk}&confirmation_token={confirmation_token}'
        except:
            return Response('Error: Could not generate valid link', status=status.HTTP_400_BAD_REQUEST)
        try:
            context['link'] = response_url
            message = BaseEmailMessage(
                template_name=email_template,
                context=context,
            )
            message.send([user_email])
            return Response('Email sent', status=status.HTTP_200_OK)
        except:
            return Response('Error: Could not send email', status=status.HTTP_406_NOT_ACCEPTABLE)

    def verify_email(self, request, pk):
        try:
            user = self.queryset.get(pk=pk)
        except:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        url = request.get_host() + f'/accounts/users/{self._ACTIVE_ACCOUNT_KEY}'
        email_template = 'emails/bootstrap_email_ev.html'
        context = {'username': user.username}
        return self.send_email(url, email_template, pk, context)

    @action(detail=False, permission_classes=[AllowAny], methods=['post'])
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
        url = request.get_host() + f'/accounts/users/{self._RESET_PASSWORD_KEY}'
        email_template = 'emails/bootstrap_email_fp.html'
        context = {}
        return self.send_email(url, email_template, user.pk, context)

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
        user.is_active = True
        user.save()
        return Response({'message': 'User activated successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, permission_classes=[AllowAny], methods=['post'])
    def reset_password(self, request):
        user_id = request.query_params.get('user_id')
        confirmation_token = request.query_params.get('confirmation_token')
        try:
            user = self.queryset.get(pk=user_id)
        except:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        new_password = request.data.get('password')
        if user.check_password(new_password):
            return Response('Insert a new password', status=status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(user, confirmation_token):
            return Response({'message': 'Invalid or expired token. Please request another confirmation email by signing in.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response('Password changed successfully', status=status.HTTP_200_OK)