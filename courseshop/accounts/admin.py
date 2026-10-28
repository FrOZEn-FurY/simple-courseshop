from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UA

from .models import *

from phonenumber_field.formfields import PhoneNumberField


class UserAdmin(UA):    
    fieldsets = [
        ("Personal Info", { "fields": ['phone_number', 'first_name', 'last_name', 'email', 'password', 'subscription', 'subscription_date_started'] })
    ]


admin.site.register(Subscription)
admin.site.register(User, UserAdmin)
admin.site.register(Token)