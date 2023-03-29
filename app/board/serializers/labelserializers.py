from django.shortcuts import get_object_or_404
from rest_framework import serializers
from accounts.serializers import *
from ..models import *


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'title', 'color', 'board']
        read_only_fields = ['id', 'board']