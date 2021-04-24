from django.contrib import admin
from .models import ProfileModel

# Register your models here.

class AdmProfile(admin.ModelAdmin):
    list_display = ('user', 'role')


admin.site.register(ProfileModel, AdmProfile)