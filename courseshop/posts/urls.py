from django.urls import path

from courseshop.views import HomeView

urlpatterns = [
    path('', HomeView, name='home'),
    path('categories/', HomeView, name='categories'),
]