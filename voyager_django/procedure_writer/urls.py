from django.urls import path

from . import views

app_name = 'procedure_writer'
urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new_procedure, name="new_procedure"),
]
