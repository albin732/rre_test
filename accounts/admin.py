from django.contrib import admin
from .models import Permission, PermissionGroup, Role

# Register your models here.


class AdmPermission(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Permission, AdmPermission)


class AdmPermissionGroup(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(PermissionGroup, AdmPermissionGroup)


class AdmRole(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Role, AdmRole)
