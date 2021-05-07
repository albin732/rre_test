from django.db import models
"""
Permission Naming_Standards
modulename_modelname_permission
core_profile_create
core_profile_read
core_profile_update
core_profile_delete
"""


class Permission(models.Model):
    name = models.CharField(max_length=255)
    codename = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "permission"
        verbose_name_plural = "permissions"


class PermissionGroup(models.Model):
    name = models.CharField(max_length=150)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "permissiongroup"
        verbose_name_plural = "permissiongroups"


class Role(models.Model):
    name = models.CharField(max_length=150)
    permission_group = models.ManyToManyField(PermissionGroup)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "role"
        verbose_name_plural = "roles"
