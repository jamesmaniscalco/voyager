from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Button, Row, Column, Div, Hidden, HTML
from crispy_forms.bootstrap import InlineField, StrictButton

from .models import Procedure, DataField, ProcedureRevision

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
            procedure_id = self.instance.procedure.id
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

    class Meta:
        model = DataField
        fields = ['name', 'field_type', 'unit']






class ProcedureRevisionMetadataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProcedureRevisionMetadataForm, self).__init__(*args, **kwargs)
        self.cancel_url=reverse_lazy('procedure_writer:edit_procedure_revision', kwargs={'procedure_id':self.instance.procedure_id, 'revision_id':self.instance.id})
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('reference_document_title'),
            Field('reference_document_URL'),
            Div(
                Div(
                    Submit('submit', 'Submit'),
                    HTML(f'<a href="{self.cancel_url}" class="btn btn-secondary">Cancel</a>'),
                ),
                css_class="form_group",
            )
        )

    class Meta:
        model = ProcedureRevision
        fields = ['reference_document_title', 'reference_document_URL']
        exclude = ['is_published', 'revision_number']