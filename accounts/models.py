from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='profile/', default='1.png')

    def __str__(self):
        return self.user.username


def user_profile(**kwargs):
    if kwargs['created']:
        profile_user = Profile(user=kwargs['instance'])
        profile_user.save()


post_save.connect(user_profile, sender=User)
