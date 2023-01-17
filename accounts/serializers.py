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


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, style={'input_type': 'password'},
                                        required=True, allow_blank=False, allow_null=False,
                                        validators=[validate_password])
    new_password = serializers.CharField(write_only=True, style={'input_type': 'password'},
                                        required=True, allow_blank=False, allow_null=False,
                                        validators=[validate_password])
    class Meta:
        model = User
        fields = ['old_password', 'new_password']

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

class ProfileOverviewSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['profile_pic', 'first_name', 'last_name', 'email', 'username']
        read_only_fields = ['profile_pic', 'first_name', 'last_name', 'email', 'username']
    
    def get_first_name(self, prof):
        return prof.user.first_name
    
    def get_last_name(self, prof):
        return prof.user.last_name
    
    def get_email(self, prof):
        return prof.user.email
    
    def get_username(self, prof):
        return prof.user.username

class EditProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['profile_pic', 'phone', 'telegram_id', 'bio', 'birth_date', 'user']
    
    def update(self, instance:Profile, validated_data):
        usr = instance.user
        prof = instance
        usr_dict = validated_data.pop('user', dict())
        prof_dict = validated_data
        profser = ProfileSerializer(instance=prof, data=prof_dict, partial=True)
        usrser = UserSerializer(instance=usr, data=usr_dict, partial=True)
        profser.is_valid(raise_exception=True)
        usrser.is_valid(raise_exception=True)
        profser.save()
        usrser.save()
        return Profile.objects.all().get(pk=instance.user.pk)