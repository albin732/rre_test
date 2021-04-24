from django.db import models
from django.contrib.auth.models import User
from accounts.models import Role, Permission


class ProfileModel(models.Model):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, null=True, blank=True)
    owner_assigned = models.ManyToManyField(
        User, related_name='owner_assigned', blank=True, default=None)
    short_name = models.CharField(max_length=7, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "profile"

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super(ProfileModel, self).save(*args, **kwargs)

    def all_permissions(self):
        return Permission.objects.filter(permissiongroup__role=self.role)
