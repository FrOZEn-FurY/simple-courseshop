from django.contrib import admin
from django.urls import path, include

from azbankgateways.urls import az_bank_gateways_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("bankgateways/", az_bank_gateways_urls()),
]
