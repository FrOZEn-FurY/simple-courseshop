from django.db import models

from accounts.models import Subscription


class Categoery(models.Model):
    title = models.CharField(max_length=100)


class Post(models.Model):
    title = models.CharField(max_length=100)
    categoery = models.ForeignKey(Categoery, on_delete=models.CASCADE, related_name='posts')
    subscription_required = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()


class PostData(models.Model):
    FILE_TYPE = (
        ('P', 'Picture'),
        ('V', 'Video'),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_files')
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(choices=FILE_TYPE, default='P')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()