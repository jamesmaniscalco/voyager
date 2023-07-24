# voyager_django URL Configuration

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("procedure_writer/", include('procedure_writer.urls'))
]
