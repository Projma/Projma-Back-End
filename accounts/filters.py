from django_filters.rest_framework import FilterSet
from .models import Profile


class ProfileFilter(FilterSet):
    class Meta:
        model = Profile
        related_fields = ['user']
        fields = {
                    'user__username': ['iexact', 'icontains'], 
                    'user__email': ['iexact', 'icontains'], 
                    'user__first_name': ['iexact', 'icontains'], 
                    'user__last_name': ['iexact', 'icontains']
                }