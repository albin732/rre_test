# from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Permission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    # codename = models.CharField(max_length=100,blank=True,null=True)
    # content_type = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "permission"
        verbose_name_plural = "permission"


class PermissionGroup(models.Model):
    name = models.CharField(max_length=150)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "permissiongroup"
        verbose_name_plural = "permissiongroup"


class Role(models.Model):
    name = models.CharField(max_length=150)
    permission_group = models.ManyToManyField(PermissionGroup)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "role"
        verbose_name_plural = "role"
