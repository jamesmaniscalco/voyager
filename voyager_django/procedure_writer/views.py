from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.template.response import TemplateResponse

from .models import Procedure, DataField
from .forms import ProcedureForm, DataFieldForm


# view that shows all Procedures.
def index(request):
    procedure_list = Procedure.objects.order_by('title')
    return render(request, 'procedure_writer/index.html', {'procedure_list': procedure_list})

# view to create a new Procedure.
def new_procedure(request):
    # GET request yields an empty form
    if request.method == 'GET':
        context = {'form': ProcedureForm()}
        return render(request, 'procedure_writer/procedure_form.html', context)
    # process a POST request by saving the entry in the database (if data conforms to specs of model).
    elif request.method == 'POST':
        form = ProcedureForm(request.POST)
        if form.is_valid():
            procedure = form.save()
            # make sure that a corresponding ProcedureRevision exists
            procedure.ensure_revision_present()
            # TODO: return a redirect to the procedure revision form
            return HttpResponseRedirect(reverse('procedure_writer:index'))

# view and/or edit a single procedure.
def view_procedure(request, procedure_id):
    procedure = get_object_or_404(Procedure, pk=procedure_id)
    return render(
        request, 
        'procedure_writer/procedure_detail.html', 
        {
            'procedure': procedure,
        },
    )

# view that serves partial template with "Add data field" button.
def add_data_field_button(request, procedure_id):
    procedure = get_object_or_404(Procedure, pk=procedure_id)
    return TemplateResponse(
        request, 
        'procedure_writer/add_data_field_button.html',
        {
            'procedure': procedure,
        }
    )

# view for serving and processing DataField forms.
def data_field_form(request, procedure_id):
    # procedure ID is handled implicitly through the URL
    procedure = get_object_or_404(Procedure, pk=procedure_id)
    if request.method == 'GET':
        data_field = DataField(procedure=procedure)
        form = DataFieldForm(instance=data_field)
        return TemplateResponse(request, 'procedure_writer/data_field_form.html', {'form': form})
    
# view for validating DataField forms.
def data_field_form_validation(request, procedure_id):
    # procedure ID is handled implicitly through the URL
    procedure = get_object_or_404(Procedure, pk=procedure_id)
    if request.method == 'POST':
        form = DataFieldForm(request.POST, procedure=procedure)
        return TemplateResponse(request, 'procedure_writer/data_field_form.html', {'form': form})
    