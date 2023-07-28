from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'procedure_writer'
urlpatterns = [
    path("", RedirectView.as_view(url="procedures/")),
    path("procedures/", views.procedure_index, name="procedure_index"),
    path("procedures/new/", views.new_procedure, name="new_procedure"),
    path("procedures/<int:procedure_id>/", views.view_procedure, name="view_procedure"),
    path("procedures/<int:procedure_id>/edit/", views.edit_procedure_metadata, name="edit_procedure_metadata"),
    path("procedures/<int:procedure_id>/delete/", views.delete_procedure, name="delete_procedure"),
    path("procedures/<int:procedure_id>/data_fields/", views.data_field_index, name="data_field_index"),
    path("procedures/<int:procedure_id>/data_fields/new/", views.new_data_field, name="new_data_field"),
    path("procedures/<int:procedure_id>/data_fields/<int:data_field_id>/edit/", views.edit_data_field, name="edit_data_field"),
    path("procedures/<int:procedure_id>/data_fields/<int:data_field_id>/delete/", views.delete_data_field, name="delete_data_field"),
]
