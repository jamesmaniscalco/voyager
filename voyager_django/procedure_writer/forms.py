from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Procedure

class ProcedureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProcedureForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Procedure
        fields = ['title']

