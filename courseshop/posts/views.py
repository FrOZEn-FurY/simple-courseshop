from typing import Any

from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect

from .models import Post, Category, UserFavorite, Comment, PostData
from .forms import *


class HomeView(ListView):
    model = Post
    queryset = Post.objects.all()
    template_name = "home_posts.html"
    paginate_by = 10


class CategoriesView(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = "categories.html"
    context_object_name = 'categories'
    

class CategoryPostsView(ListView):
    models = Post
    template_name = 'category_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(category=self.category)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        category = self.category
        ancestors = []
        while category:
            ancestors.append(category)
            category = category.parent
        ancestors.reverse()
        context['ancestors'] = ancestors
        return context


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_detail.html'

    def get_object(self, queryset: QuerySet[Any, Any] | None = None) -> Model:
        return Post.objects.get(pk=self.kwargs['pk'], category__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        category = context['post'].category
        ancestors = []
        while category:
            ancestors.append(category)
            category = category.parent
        ancestors.reverse()
        context['ancestors'] = ancestors
        
        recent = Post.objects.filter(category=category)[:3]
        context['recent'] = recent

        try:
            liked = UserFavorite.objects.get(post=context['post'], user=self.request.user)
        except ObjectDoesNotExist:
            liked = None
        context['liked'] = liked

        comments = Comment.objects.filter(post=context['post'])
        context['comments'] = comments

        comment_form = CommentForm()
        context['comment_form'] = comment_form

        files = PostData.objects.filter(post=context['post'])
        context['files'] = files
            
        return context


class AddToFavoriteView(LoginRequiredMixin, View):
    def get(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        try:
            favorite = UserFavorite.objects.get(post=post, user=request.user)
            favorite.delete()
            messages.success(request, "Removed from favorites successfully.")
        except ObjectDoesNotExist:
            UserFavorite.objects.create(post=post, user=request.user)
            messages.success(request, "Added from favorites successfully.")
        return redirect('post-detail', slug=post.category.slug, pk=post.pk)


class AddComment(LoginRequiredMixin, View):
    def post(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Comment sent successfully.")
        else:
            messages.error(request, "Invalid Form Values.")
        return redirect('post-detail', slug=post.category.slug, pk=post.pk)