# products/urls.py
from django.contrib import admin
from django.urls import path

from products import views as pv


urlpatterns = [
    path("admin/", admin.site.urls),
    path("pricing/", pv.home, name="home"),
    path("success/", pv.success, name="success"),
    path("cancel/", pv.cancel, name="cancel"),
]