from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Button, Row, Column, Div
from crispy_forms.bootstrap import InlineField

from .models import Procedure, DataField

# Form class for basic Procedure information
class ProcedureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProcedureForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Procedure
        fields = ['title']


# Form for a DataField
class DataFieldForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DataFieldForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper.layout = Layout(
        #     Field('name'),
        #     Field('field_type'),
        #     Field('unit'),
        #     Submit('submit', 'Submit'),
        #     Button('cancel', 'Cancel'),
        # )
        # self.helper.form_show_labels = False
        if self.instance.field_type in ("float", "int"):
            self.instance.unit = ''

        self.helper.layout = Layout(
            Div(
                Div(
                    InlineField('name', wrapper_class='input-group-sm'), 
                    css_class='col-4 py-2 d-flex align-items-center border border-top-0',
                ),
                Div(
                    InlineField('field_type', wrapper_class='input-group-sm'), 
                    css_class='col-2 py-2 d-flex align-items-center border-right border-bottom',
                ),
                Div(
                    InlineField('unit', wrapper_class='input-group-sm') if self.instance.field_type in ("float", "int") else InlineField('unit', wrapper_class='input-group-sm', disabled=True), 
                    css_class='col-2 py-2 d-flex align-items-center border-right border-bottom',
                ),
                Div(
                    css_class='col-2 py-2 d-flex align-items-center border-right border-bottom',
                ),
                Div(
                    Submit('submit', 'Submit', css_class="btn-sm"),
                    Button(
                        'cancel', 
                        'Cancel', 
                        css_class="btn-secondary btn-sm",
                        hx_get=reverse_lazy('procedure_writer:add_data_field_button', kwargs={'procedure_id':self.instance.procedure.id}),
                        hx_target="#data_fields_table_bottom_row",
                    ),
                    css_class='col-2 py-2 my-auto border-right border-bottom',
                ),
                css_class='row',
            )
        )
        self.helper.form_show_labels = False
        self.helper.form_class = 'col'

    class Meta:
        model = DataField
        fields = ['procedure', 'name', 'field_type', 'unit']