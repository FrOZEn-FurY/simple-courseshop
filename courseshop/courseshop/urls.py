from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from azbankgateways.urls import az_bank_gateways_urls

from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("bankgateways/", az_bank_gateways_urls()),
    path("accounts/", include("accounts.urls")),
    path("", include("posts.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
