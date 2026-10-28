from typing import Any

import pytz

from datetime import timedelta

from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import FormView, View, UpdateView
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from formtools.wizard.views import SessionWizardView

from .forms import *
from .models import User


class LoginView(FormView):
    form_class = LoginForm
    template_name = "login_form.html"
    success_url = "/"

    def form_valid(self, form):
        user = authenticate(self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user:
            login(self.request, user)
            messages.success(self.request, "Login Successful.")
            return super().form_valid(form)
        messages.error(self.request, "Invalid form values.")
        return redirect('login')

    def form_invalid(self, form):
        messages.error(self.request, "Invalid form values.")
        response = super().form_invalid(form)
        return response


class SignupWizard(SessionWizardView):
    form_list = [PhoneNumberForm, TokenForm, SignupForm]
    template_name = "signup_form.html"

    def done(self, form_list, **kwargs):
        password = form_list[2].cleaned_data['password']
        phone_number = form_list[0].cleaned_data['phone_number']
        form_list[2].cleaned_data.pop('password')
        form_list[2].cleaned_data.pop('confirm_password')
        User.objects.create_user(**form_list[2].cleaned_data, password=password, username=phone_number, phone_number=phone_number)
        messages.success(self.request, "Signup successful.")
        return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logout successful.")
        return redirect("home")


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "profile_form.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        if self.request.user.subscription:
            now = timezone.datetime.now()
            expiration_date = self.request.user.subscription_date_started.astimezone(pytz.timezone("Asia/Tehran")) + timedelta(days=self.request.user.subscription.duration)
            difference = expiration_date - timezone.make_aware(now, pytz.timezone("Asia/Tehran"))
            data['time_remaining'] = difference.days
        return data


class ChangePasswordView(LoginRequiredMixin, FormView):
    form_class = ChangePasswordForm
    template_name = "change_password_form.html"
    success_url = '/accounts/profile'

    def form_valid(self, form):
        if self.request.user.check_password(form.cleaned_data['current_password']):
            self.request.user.set_password(form.cleaned_data['password'])
            messages.success(self.request, "Password Chagned Successfully.")
            self.request.user.save()
            return redirect('login')
        messages.error(self.request, "Your current password is invalid.")    
        return redirect('change-password')

    def form_invalid(self, form):
        messages.error(self.request, "Invalid form values.")
        response = super().form_invalid(form)
        return response
    