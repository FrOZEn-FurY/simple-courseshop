from django.urls import path

from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupWizard.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password')
]