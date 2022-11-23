from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import *

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'},
                                        required=True, allow_blank=False, allow_null=False,
                                        validators=[validate_password])
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']

    def create(self, validated_data):
        new_user = User.objects.create_user(**validated_data)
        new_user.set_password(validated_data['password'])
        return new_user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email']
        read_only_fields = ('id', 'username', 'password', 'email')


class PublicInfoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ('id', 'username', 'password')


class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    class Meta:
        model = User
        fields = ['email']


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'},
                                        required=True, allow_blank=False, allow_null=False,
                                        validators=[validate_password])
    class Meta:
        model = User
        fields = ['password']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=False)
    class Meta:
        model = Profile
        fields = ['user', 'birth_date', 'bio', 'phone', 'profile_pic', 'telegram_id']


class PublicInfoProfileSerializer(serializers.ModelSerializer):
    user = PublicInfoUserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'profile_pic']