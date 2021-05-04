from django.db import models
from django.contrib.auth.models import User
from accounts.models import Role, Permission

"""
Three users
master_admin, sub_admin, client
"""


# class ProfileQuerySet(models.QuerySet):
#     def master_admin(self, user):
#         return self.filter(role=Role.objects.get(name='master_admin').id).filter(user=user).count()

#     def sub_admin(self, user):
#         return self.filter(role=Role.objects.get(name='sub_admin').id).filter(user=user).count()

#     def client(self, user):
#         return self.filter(role=Role.objects.get(name='client').id).filter(user=user).count()


class ProfileManager(models.Manager):
    # def get_queryset(self):
    #     return ProfileQuerySet(self.model, using=self._db)

    def is_masteradmin(self, user):
        return self.filter(role=Role.objects.get(name='master_admin').id).filter(user=user).count()

    def is_subadmin(self, user):
        return self.filter(role=Role.objects.get(name='sub_admin').id).filter(user=user).count()

    def is_client(self, user):
        return self.filter(role=Role.objects.get(name='client').id).filter(user=user).count()


class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, null=True, blank=True)
    owner_assigned = models.ManyToManyField(
        User, related_name='owner_assigned', blank=True, default=None)
    short_name = models.CharField(max_length=7, null=True, blank=True)
    # is_active = models.BooleanField(default=True)

    objects = models.Manager()
    profiles = ProfileManager()

    class Meta:
        db_table = "profile"

    def __str__(self):
        return str(self.user)

    # def is_masteradmin(self):
    #     return str(self.role) == 'master_admin'

    # def is_subadmin(self):
    #     return str(self.role) == 'sub_admin'

    # def is_client(self):
    #     return str(self.role) == 'client'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

    def all_permissions(self):
        return Permission.objects.filter(permissiongroup__role=self.role)
