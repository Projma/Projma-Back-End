from rest_framework import serializers
from .models import *


class CRUDUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email']
        read_only_fields = ('id', 'username', 'password', 'email')


class CRUDProfileSerializer(serializers.ModelSerializer):
    user = CRUDUserSerializer(read_only=False)
    class Meta:
        model = Profile
        fields = ['user', 'birth_date', 'bio', 'phone', 'profile_pic', 'telegram_id']


class CRUDWorkspaceSerializer(serializers.ModelSerializer):
    boards = serializers.PrimaryKeyRelatedField(read_only = True, many=True)
    class Meta:
        model = WorkSpace
        fields = ['id', 'name', 'description', 'type', 'created_at', 'updated_at', 'owner', 'members', 'boards']
        read_only_fields = ('id', 'created_at', 'updated_at')


class CRUDBoardSerializer(serializers.ModelSerializer):
    tasklists = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'background_pic', 'workspace', 
                    'created_at', 'updated_at', 'admins', 'members', 'tasklists']
        read_only_fields = ('id', 'created_at', 'updated_at')

class CRUDLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'board', 'title', 'color']
        read_only_fields = ['id', 'board']