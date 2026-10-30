from django.db import models
from django.urls import reverse_lazy

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

from ckeditor.fields import RichTextField

from accounts.models import User

class Category(MPTTModel):
    name = models.CharField(
        max_length=200,
        unique=True,
    )
    slug = models.SlugField(
        max_length=300,
        unique=True,
        null=True,
        blank=True,
        allow_unicode=True
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='category_parent'
    )

    def get_absolute_url(self):
        return reverse_lazy('category-posts', args=(self.slug,))


class Post(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_posts')
    subscription_required = models.BooleanField(default=False)
    body = RichTextField()

    def get_absolute_url(self):
        return reverse_lazy('post-detail', args=(self.category.slug, self.pk))


class PostData(models.Model):
    FILE_TYPE = (
        ('P', 'Picture'),
        ('V', 'Video'),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_files')
    file = models.ImageField(upload_to='uploads/', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    file_type = models.CharField(choices=FILE_TYPE, default='P')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = RichTextField()
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)


class UserFavorite(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorited')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')