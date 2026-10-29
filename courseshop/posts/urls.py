from django.urls import path

from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('categories/<str:slug>', CategoryPostsView.as_view(), name='category-posts'),
    path('categories/<str:slug>/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('add-to-favorite/<int:post_pk>', AddToFavoriteView.as_view(), name='add-to-favorite'),
    path('add-comment/<int:post_pk>', AddComment.as_view(), name='add-comment'),
]