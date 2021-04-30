from django.contrib import admin
from .models import ProfileModel
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


class AdmProfile(admin.ModelAdmin):
    list_display = ('user', 'role')


admin.site.register(ProfileModel, AdmProfile)


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'first_name',
                    'is_active', 'is_staff', 'is_superuser', 'last_login')


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
