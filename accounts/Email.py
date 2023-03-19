from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.response import Response
from templated_mail.mail import BaseEmailMessage

class SendEmail:
    def __init__(self, queryset) -> None:
        self.queryset = queryset

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
            # context['link'] = 'https://www.google.com'
            message = BaseEmailMessage(
                template_name=email_template,
                context=context,
            )
            message.send([user_email])
            return Response('Email sent', status=status.HTTP_200_OK)
        except:
            return Response('Error: Could not send email', status=status.HTTP_406_NOT_ACCEPTABLE)
