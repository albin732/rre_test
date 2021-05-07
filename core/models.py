from django.db import models
from django.contrib.auth.models import User
from accounts.models import Role, Permission


"""
Three Types of users in django default User
master_admin, sub_admin, client
"""


class ProfileManager(models.Manager):

    def is_masteradmin(self, user):
        return self.filter(role=Role.objects.get(name='master_admin').id, user=user).count()

    def is_subadmin(self, user):
        return self.filter(role=Role.objects.get(name='sub_admin').id, user=user).count()

    def is_client(self, user):
        return self.filter(role=Role.objects.get(name='client').id, user=user).count()

    def all_permissions(self, user):
        return Permission.objects.filter(permissiongroup__role=self.filter(user=user).first().role)


'''User Profile'''


class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, null=True, blank=True)
    owner_assigned = models.ManyToManyField(
        User, related_name='owner_assigned', blank=True, default=None)
    short_name = models.CharField(max_length=7, null=True, blank=True)

    objects = models.Manager()
    profiles = ProfileManager()

    class Meta:
        db_table = "profile"

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
