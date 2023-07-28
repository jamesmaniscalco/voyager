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
    #path("procedure_detail/<int:procedure_id>/data_field_form/", views.data_field_form, name="data_field_form"),
    #path("procedure_detail/<int:procedure_id>/data_field_form/validate/", views.data_field_form_validation, name="data_field_form_validation"),
    #path("procedure_detail/<int:procedure_id>/add_data_field_button/", views.add_data_field_button, name="add_data_field_button"),
]
