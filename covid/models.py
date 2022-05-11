from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class DailyDictionary(models.Model):
    pulse = models.FloatField(max_length=3)
    temperature = models.FloatField(max_length=3)
    exercises = models.CharField(max_length=50)
    sleep_time = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class UserCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    first_name = models.CharField(max_length=40, null=False)
    second_name = models.CharField(max_length=40, null=False)
    last_name = models.CharField(max_length=40)
    sex = models.CharField(max_length=10)
    age = models.IntegerField()
    diagnosis = models.CharField(max_length=90)
    comment = models.CharField(max_length=150)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


admin.site.register(UserCard)
admin.site.register(DailyDictionary)
