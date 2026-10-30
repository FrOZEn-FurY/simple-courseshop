from typing import Any

import pytz

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from datetime import timedelta

from .models import *
from .utils import send_otp

from phonenumber_field.formfields import PhoneNumberField


class LoginForm(forms.Form):
    username = PhoneNumberField(region='IR')
    password = forms.CharField(widget=forms.PasswordInput)


class PhoneNumberForm(forms.Form):
    phone_number = PhoneNumberField(region='IR')

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        send_otp(self.cleaned_data['phone_number'])
        return cleaned_data


class TokenForm(forms.Form):
    token = forms.CharField(max_length=5)

    def clean(self):
        cleaned_data = super(TokenForm, self).clean()
        phone_number = self.initial['phone_number']
        try:
            db_token = Token.objects.get(value=self.cleaned_data['token'], phone_number=phone_number)
            time_differnece = timezone.datetime.now() - timedelta(minutes=2)
            print(timezone.make_aware(time_differnece), db_token.date_created.astimezone(pytz.timezone('Asia/Tehran')))
            if timezone.make_aware(time_differnece) > db_token.date_created.astimezone(pytz.timezone('Asia/Tehran')):
                self.add_error('token', 'Token is expired.')
        except ObjectDoesNotExist:
            self.add_error('token', "Token is invalid.")
        return cleaned_data

            

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def clean(self) -> dict[str, Any]:
        cleaned_data =  super().clean()
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            self.add_error('confirm_password', "Passwords don't match.")
        return cleaned_data


class ProfileForm(forms.ModelForm):
    phone_number = PhoneNumberField(region='IR')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number']


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self) -> dict[str, Any]:
        cleaned_data =  super().clean()
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            self.add_error('confirm_password', "Passwords don't match.")
        return cleaned_data