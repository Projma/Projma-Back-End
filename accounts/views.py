from django.contrib.auth.tokens import default_token_generator
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
    serializer_class = CreateUserSerializer

    def get_permissions(self):
        if self.request.method == 'GET' and \
            not 'active' in self.request.path:
                return [IsAdminUser()]
        return [AllowAny()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        pk = serializer.instance.pk
        self.send_verify_email(request, pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def send_verify_email(self, request, pk):
        try:
            user = self.queryset.get(pk=pk)
            user_email = user.email
            confirmation_token = default_token_generator.make_token(user)
        except:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        try:
            activate_url_link = request.get_host() + '/accounts/users/active' #?
            activation_link = f'{activate_url_link}?user_id={user.pk}&confirmation_token={confirmation_token}'
        except:
            return Response('Error: Could not generate activation link', status=status.HTTP_400_BAD_REQUEST)
        try:
            message = BaseEmailMessage(
                template_name='emails/bootstrap_email_ev.html',
                context={'username': user.username,
                            'activate_link': activation_link},
            )
            message.send([user_email])
            return Response('Email sent', status=status.HTTP_200_OK)
        except:
            return Response('Error: Could not send email', status=status.HTTP_406_NOT_ACCEPTABLE)

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