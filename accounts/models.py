from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Permissions(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "permissions"

class PermissionGroup(models.Model):
    name = models.CharField(max_length=15)
    permissions = models.ManyToManyField(Permissions)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "permissiongroup"

class Roles(models.Model):
    name = models.CharField(max_length=15)
    permission_group = models.ManyToManyField(PermissionGroup)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "roles"


class User(AbstractUser):
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True, blank=True)
