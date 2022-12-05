from django.shortcuts import get_object_or_404
from rest_framework import serializers
from accounts.serializers import *
from .labelserializers import *
from ..models import *

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'sender', 'task', 'reply_to', 'created_at', 'updated_at']
        read_only_fields = ['id', 'sender', 'task', 'reply_to', 'created_at', 'updated_at']