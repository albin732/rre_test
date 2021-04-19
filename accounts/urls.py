from django.urls import path

from accounts.views import UserPermissions

urlpatterns = [
    path('permissions/', UserPermissions.as_view(), name='user-permissions')
]
