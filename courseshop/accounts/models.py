from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField


class Token(models.Model):
    value = models.CharField(max_length=5)
    date_created = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    title = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    price = models.PositiveIntegerField()


class User(AbstractUser):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    phone_number = PhoneNumberField(unique=True)
    subscription_date_started = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "phone_number"

    def __str__(self) -> str:
        return self.phone_number.__str__()