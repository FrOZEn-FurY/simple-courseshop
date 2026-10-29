from django import forms

from .models import Comment, Post, PostData

from ckeditor_uploader.fields import RichTextUploadingFormField


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'