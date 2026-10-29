from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import *
from .forms import PostAdminForm

class PostDataInline(admin.TabularInline):
    model = PostData


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    fieldsets = [
        ("Post", { "fields": ["title", "category", "subscription_required", "body"], "description": "The core data of a post." }),
    ]
    inlines = [PostDataInline]

admin.site.register(Category, MPTTModelAdmin)
admin.site.register(PostData)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(UserFavorite)