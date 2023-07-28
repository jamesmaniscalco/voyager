from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Button, Row, Column, Div, Hidden, HTML
from crispy_forms.bootstrap import InlineField, StrictButton

from .models import Procedure, DataField

# Form class for basic Procedure information
class ProcedureMetadataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProcedureMetadataForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        if self.instance.pk:
            self.cancel_url=reverse_lazy('procedure_writer:view_procedure', kwargs={'procedure_id':self.instance.id})
        else:
            self.cancel_url=reverse_lazy('procedure_writer:procedure_index')
        self.helper.layout.append(
            Div(
                Div(
                    Submit('submit', 'Submit'),
                    HTML(f'<a href="{self.cancel_url}" class="btn btn-secondary">Cancel</a>'),
                ),
                css_class="form_group",
            )
        )

    class Meta:
        model = Procedure
        fields = ['title']




class DataFieldForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'procedure_id' in kwargs:
            procedure_id = kwargs.pop('procedure_id')
        super(DataFieldForm, self).__init__(*args, **kwargs)
        if hasattr(self.instance, 'procedure'):
            self.cancel_url=reverse_lazy('procedure_writer:data_field_index', kwargs={'procedure_id':self.instance.procedure.id})
        else:
            self.cancel_url=reverse_lazy('procedure_writer:data_field_index', kwargs={'procedure_id':procedure_id})
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('name'),
            Field('field_type'),
            Field('unit'),
            Div(
                Div(
                    Submit('submit', 'Submit'),
                    HTML(f'<a href="{self.cancel_url}" class="btn btn-secondary">Cancel</a>'),
                ),
                css_class="form_group",
            )
        )

        if self.fields['field_type'] not in ('int', 'float'):
            self.instance.unit = ''
            self.fields['unit'].disabled = True
        else:
            self.fields['unit'].disabled = False

    class Meta:
        model = DataField
        fields = ['name', 'field_type', 'unit']









# # Form for a DataField
# class DataFieldForm(forms.ModelForm):
#     def __init__(self, procedure, *args, **kwargs):
#         super(DataFieldForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         # self.helper.layout = Layout(
#         #     Field('name'),
#         #     Field('field_type'),
#         #     Field('unit'),
#         #     Submit('submit', 'Submit'),
#         #     Button('cancel', 'Cancel'),
#         # )
#         # self.helper.form_show_labels = False
#         if self.instance.field_type in ("float", "int"):
#             self.instance.unit = ''

#         self.helper.form_tag = False
#         #self.helper.form_action = reverse_lazy('procedure_writer:data_field_form', kwargs={'procedure_id':self.instance.procedure.id})
#         self.helper.layout = Layout(
#             Div(
#                 Div(
#                     InlineField('name', wrapper_class='input-group-sm'), 
#                     css_class='col-4 py-2 d-flex align-items-center border border-top-0',
#                 ),
#                 Div(
#                     InlineField(
#                         'field_type', 
#                         wrapper_class='input-group-sm',
#                     ), 
#                     css_class='col-2 py-2 d-flex align-items-center border-right border-bottom',
#                 ),
#                 Div(
#                     InlineField('unit', wrapper_class='input-group-sm') if self.instance.field_type in ("float", "int") else InlineField('unit', wrapper_class='input-group-sm', disabled=True), 
#                     css_class='col-2 py-2 d-flex align-items-center border-right border-bottom',
#                 ),
#                 Div(
#                     css_class='col-2 py-2 d-flex align-items-center border-right border-bottom',
#                 ),
#                 Div(
#                     Submit('submit', 'Submit', css_class="btn-sm"),
#                     Button(
#                         'cancel', 
#                         'Cancel', 
#                         css_class="btn-secondary btn-sm",
#                         hx_get=reverse_lazy('procedure_writer:add_data_field_button', kwargs={'procedure_id':procedure.id}),
#                         hx_target="#data_fields_table_bottom_row",
#                     ),
#                     css_class='col-2 py-2 my-auto border-right border-bottom',
#                 ),
#                 css_class='row',
#             )
#         )
#         self.helper.form_show_labels = False
#         self.helper.form_class = 'col'

#     class Meta:
#         model = DataField
#         fields = ['procedure', 'name', 'field_type', 'unit']