from django.shortcuts import get_object_or_404
from rest_framework import serializers
from accounts.serializers import *
from ..models import *


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['file', 'id', 'task', 'user', 'created_at', 'updated_at']
        read_only_fields = ['id', 'task', 'user', 'created_at', 'updated_at']