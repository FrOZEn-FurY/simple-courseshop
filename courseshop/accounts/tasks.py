from celery import shared_task

from .models import User, Token

from django.utils import timezone

import pytz

@shared_task
def remove_subscriptions():
    users = User.objects.all()
    for user in users:
        date_started = user.subscription_date_started
        if date_started and user.subscription:
            expirtaion_date = date_started.astimezone(pytz.timezone('Asia/Tehran')) + timezone.timedelta(days=user.subscription.duration)
            if expirtaion_date < timezone.now():
                user.subscription = None
                user.subscription_date_started = None
                user.save()


@shared_task
def remove_tokens():
    tokens = Token.objects.all()
    for token in tokens:
        two_mintues_ago = timezone.now() - timezone.timedelta(minutes=2)
        if token.date_created < two_mintues_ago:
            token.delete()