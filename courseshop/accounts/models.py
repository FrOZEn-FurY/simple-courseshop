from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from phonenumber_field.modelfields import PhoneNumberField


class Subscription(models.Model):
    title = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()


class User(AbstractBaseUser):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    phone_number = PhoneNumberField(unique=True)
    subscription_date_started = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "phone_number"