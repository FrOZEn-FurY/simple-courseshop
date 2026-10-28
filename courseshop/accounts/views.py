from typing import Any

import pytz

from datetime import timedelta

from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import FormView, View, UpdateView, ListView, TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import Http404

from azbankgateways import models as bank_models, default_settings as settings, bankfactories

from formtools.wizard.views import SessionWizardView

from .forms import *
from .models import User, Subscription


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


class SubscriptionListView(LoginRequiredMixin, ListView):
    model = Subscription
    queryset = Subscription.objects.all()
    template_name = "subscription_list.html"


class CallbackGatewayView(TemplateView):
    template_name = 'callback_gateway.html'

    def get(self, request):
        tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
        if not tracking_code:
            raise Http404
    
        try:
            bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
        except bank_models.Bank.DoesNotExist:
            raise Http404
    
        if bank_record.is_success:
            return render(request, self.template_name, context={ 'message': "پرداخت با موفقیت انجام شد." })
    
        return render(request, self.template_name, context={ 'message': "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت." })


class BuySubscriptionView(View):
    def get(self, request, pk):
        sub = Subscription.objects.get(pk=pk)
        factory = bankfactories.BankFactory()
        bank = factory.create()
        bank.set_request(request)
        bank.set_amount(sub.price)
        bank.set_client_callback_url(reverse('callback-gateway'))
        bank.ready()
    
        return bank.redirect_gateway()