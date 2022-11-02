from dataclasses import fields
from pyexpat import model
from importlib_metadata import files
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
