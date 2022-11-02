from django.forms import ValidationError
from rest_framework import serializers
from .models import *

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']

    def create(self, validated_data):
        new_user = User.objects.create_user(**validated_data)
        new_user.set_password(validated_data['password'])
        return new_user
