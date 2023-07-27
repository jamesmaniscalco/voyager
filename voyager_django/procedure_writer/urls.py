from django.urls import path

from . import views

app_name = 'procedure_writer'
urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new_procedure, name="new_procedure"),
    path("procedure_detail/<int:procedure_id>/", views.view_procedure, name="view_procedure"),
    path("procedure_detail/<int:procedure_id>/data_field_form/", views.data_field_form, name="data_field_form"),
    path("procedure_detail/<int:procedure_id>/data_field_form/validate/", views.data_field_form_validation, name="data_field_form_validation"),
    path("procedure_detail/<int:procedure_id>/add_data_field_button/", views.add_data_field_button, name="add_data_field_button"),
]
