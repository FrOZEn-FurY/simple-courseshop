from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import *
from .forms import PostDataAdminFormset


class PostDataInline(admin.StackedInline):
    model = PostData
    formset = PostDataAdminFormset


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Post", { "fields": ["title", "category", "subscription_required", "body"], "description": "The core data of a post." }),
    ]
    inlines = [PostDataInline]

admin.site.register(Category, MPTTModelAdmin)
admin.site.register(PostData)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(UserFavorite)