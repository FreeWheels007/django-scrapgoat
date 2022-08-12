from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from pathlib import Path
from uuid import uuid4


class User(AbstractUser):
    pass


class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    cell = models.CharField(max_length=200, blank=True, null=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


def image_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'user{instance.user.id}_{uuid4().hex}.{ext}'
    return Path('images/') / filename


class Pickup(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELLED = 'CANCELLED', _('Cancelled')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=200, blank=True, null=True)
    cell = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    details = models.CharField(max_length=500)
    scrap_image = models.ImageField(blank=True, null=True, upload_to=image_file_name)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    date_posted = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_finished = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'name={self.name}, email={self.email}, loc={self.location}, status={self.status}' \
               f'created={self.date_posted}, finished={self.date_finished}'


class UserSavedLocation(models.Model):

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f'address={self.address}'
