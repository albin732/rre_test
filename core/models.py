from django.db import models

# Create your models here.
from accounts.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


class ClientsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


# client model
class Client(models.Model):
    name = models.CharField(max_length=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    owner_assigned = models.ManyToManyField(User,related_name='owner_assigned')
    short_name = models.CharField(max_length=7)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    actives = ClientsManager()

    def __str__(self):
        return self.name


# client config
class ClientConfig(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    db_name = models.CharField(max_length=15)
    host = models.CharField(max_length=30, default='localhost')
    port = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.client.name + " db config"


# custom user
@receiver(pre_save, sender=ClientConfig)
def mongo_db(sender, instance, *args, **kwargs):
    # here, Check if user is not master_admin , sub_admin
    if not instance.db_name:
        instance.db_name = "db_" + instance.client.name.replace(' ', '').lower()
