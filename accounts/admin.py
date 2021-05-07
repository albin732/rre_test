from django.contrib import admin
from .models import Permission, PermissionGroup, Role

# Register your models here.


class AdmPermission(admin.ModelAdmin):
    list_display = ('name',)


class AdmPermissionGroup(admin.ModelAdmin):
    list_display = ('name',)


class AdmRole(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Permission, AdmPermission)
admin.site.register(PermissionGroup, AdmPermissionGroup)
admin.site.register(Role, AdmRole)
