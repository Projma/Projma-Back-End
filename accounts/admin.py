from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password',\
              'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login']
    readonly_fields = ['id', 'email', 'password', 'date_joined', 'last_login']
class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)