from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse
from django.template.response import TemplateResponse

from .models import Procedure, DataField
from .forms import ProcedureForm, DataFieldForm


# view that shows all Procedures.
def procedure_index(request):
    procedure_list = Procedure.objects.order_by('title')
    return render(request, 'procedure_writer/procedure_index.html', {'procedure_list': procedure_list})

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
            return HttpResponseRedirect(reverse('procedure_writer:procedure_index'))
        else:
            context = {'form': form}
            return render(request, 'procedure_writer/procedure_form.html', context)

# view a single procedure and its details.
def view_procedure(request, procedure_id):
    procedure = get_object_or_404(Procedure, pk=procedure_id)
    context = {'procedure': procedure}
    return render(request, 'procedure_writer/procedure_detail.html', context)

# edit the metadata of a procedure (i.e. not data specific to a revision).
def edit_procedure_metadata(request, procedure_id):
    procedure = get_object_or_404(Procedure, pk=procedure_id)
    form = ProcedureForm(request.POST or None, instance=procedure)
    if form.is_valid():
        form.save()
        return redirect('procedure_writer:view_procedure', procedure_id=procedure.id)
    else:
        context = {'form': form}
        return render(request, 'procedure_writer/procedure_form.html', context)

# delete a procedure.
# TODO: logic to make sure that procedures only deleted if no published revisions.
def delete_procedure(request, procedure_id):
    procedure = get_object_or_404(Procedure, pk=procedure_id)
    if request.method == 'POST':
        procedure.delete()
        return redirect('procedure_writer:procedure_index')
    else:
        context = {'procedure': procedure}
        return render(request, 'procedure_writer/procedure_confirm_delete.html', context)

    






# view that serves partial template with "Add data field" button.
def add_data_field_button(request, procedure_id):
    procedure = get_object_or_404(Procedure, pk=procedure_id)
    return TemplateResponse(request, 'procedure_writer/add_data_field_button.html', context={'procedure':procedure})

# view for serving and processing DataField forms.
def data_field_form(request, procedure_id):
    # procedure ID is handled implicitly through the URL
    procedure = get_object_or_404(Procedure, pk=procedure_id)
    if request.method == 'GET':
        form = DataFieldForm(procedure=procedure)
        return TemplateResponse(request, 'procedure_writer/data_field_form.html', {'form': form, 'procedure':procedure})
    if request.method == 'POST':
        form = DataFieldForm(initial=request.POST, procedure=procedure)
        data_field = form.save(commit=False)
        return TemplateResponse(request, 'procedure_writer/data_field_form.html', {'form': form, 'procedure':procedure})

    
# view for validating DataField forms.
def data_field_form_validation(request, procedure_id):
    # procedure ID is handled implicitly through the URL
    procedure = get_object_or_404(Procedure, pk=procedure_id)
    if request.method == 'POST':
        form = DataFieldForm(request.POST, procedure=procedure)
        return TemplateResponse(request, 'procedure_writer/data_field_form.html', {'form': form})
    