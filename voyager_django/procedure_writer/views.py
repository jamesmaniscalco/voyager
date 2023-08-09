from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse
from django.http import Http404, HttpResponseForbidden
from django.template.response import TemplateResponse
from django.core.exceptions import PermissionDenied, BadRequest

from .models import Procedure, DataField, ProcedureRevision
from .forms import ProcedureMetadataForm, DataFieldForm, ProcedureRevisionMetadataForm


### Procedures

# view that shows all Procedures.
def procedure_index(request):
    procedure_list = Procedure.objects.order_by('title')
    return render(request, 'procedure_writer/procedure_index.html', {'procedure_list': procedure_list})

# view to create a new Procedure.
def new_procedure(request):
    # GET request yields an empty form
    if request.method == 'GET':
        context = {
            'form': ProcedureMetadataForm(),
            'page_title': "New Procedure",
        }
        return render(request, 'procedure_writer/procedure_metadata_form.html', context)
    # process a POST request by saving the entry in the database (if data conforms to specs of model).
    elif request.method == 'POST':
        form = ProcedureMetadataForm(request.POST)
        if form.is_valid():
            procedure = form.save()
            # make sure that a corresponding ProcedureRevision exists
            procedure.ensure_revision_present()
            # TODO: return a redirect to the procedure revision form
            return HttpResponseRedirect(reverse('procedure_writer:procedure_index'))
        else:
            context = {
                'form': form,
                'page_title': "New Procedure",
            }
            return render(request, 'procedure_writer/procedure_metadata_form.html', context)

# view a single procedure and its details.
def view_procedure(request, procedure_id):
    procedure = get_object_or_404(Procedure, pk=procedure_id)
    context = {'procedure': procedure}
    return render(request, 'procedure_writer/procedure_detail.html', context)

# edit the metadata of a procedure (i.e. not data specific to a revision).
def edit_procedure_metadata(request, procedure_id):
    procedure = get_object_or_404(Procedure, pk=procedure_id)
    form = ProcedureMetadataForm(request.POST or None, instance=procedure)
    if form.is_valid():
        form.save()
        return redirect('procedure_writer:view_procedure', procedure_id=procedure.id)
    else:
        context = {
            'form': form,
            'page_title': "Edit Procedure Metadata",
        }
        return render(request, 'procedure_writer/procedure_metadata_form.html', context)

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

    




### DataFields

# data fields index view.
def data_field_index(request, procedure_id):
    procedure = get_object_or_404(Procedure, pk=procedure_id)
    context = {'procedure': procedure}
    return render(request, 'procedure_writer/data_field_index.html', context)

def new_data_field(request, procedure_id):
    procedure = get_object_or_404(Procedure, pk=procedure_id)
    # GET request yields an empty form
    if request.method == 'GET':
        form = DataFieldForm(procedure_id=procedure.id)
        form.instance.procedure = procedure
    # process a POST request by saving the entry in the database (if data conforms to specs of model).
    elif request.method == 'POST':
        form = DataFieldForm(request.POST, procedure_id=procedure.id)
        form.instance.procedure = procedure
        if form.is_valid():
            data_field = form.save()
            return HttpResponseRedirect(reverse('procedure_writer:data_field_index', kwargs={'procedure_id':data_field.procedure.id}))
    context = {'form': form,
                'page_title': "New Data Field",
                'procedure_title': procedure.title}
    return render(request, 'procedure_writer/data_field_form.html', context)

# logic for handling if supposedly related objects are not in fact related.
def get_procedure_and_data_field_or_raise_error(procedure_id, data_field_id):
    procedure = get_object_or_404(Procedure, pk=procedure_id)
    data_field = get_object_or_404(DataField, pk=data_field_id)
    if data_field.procedure != procedure:
        raise BadRequest("The requested Data Field and Procedure are not associated with each other.")
    return procedure, data_field

# edit the attributes of a DataField.
def edit_data_field(request, procedure_id, data_field_id):
    procedure, data_field = get_procedure_and_data_field_or_raise_error(procedure_id, data_field_id)
    form = DataFieldForm(request.POST or None, instance=data_field)
    if form.is_valid():
        form.save()
        return redirect('procedure_writer:data_field_index', procedure_id=procedure.id)
    else:
        context = {
            'form': form,
            'page_title': "Edit Data Field",
            'procedure_title': procedure.title,
        }
        return render(request, 'procedure_writer/data_field_form.html', context)

# delete a data field.
# TODO: logic to make sure that DataFields only deleted if no entries and not in any revision.
def delete_data_field(request, procedure_id, data_field_id):
    procedure, data_field = get_procedure_and_data_field_or_raise_error(procedure_id, data_field_id)
    if request.method == 'POST':
        data_field.delete()
        return redirect('procedure_writer:data_field_index', procedure_id=procedure.id)
    else:
        context = {'data_field': data_field}
        return render(request, 'procedure_writer/data_field_confirm_delete.html', context)







### ProcedureRevisions

# Create a new procedure revision.
def new_procedure_revision(request, procedure_id):
    if request.method=='POST':
        procedure = get_object_or_404(Procedure, pk=procedure_id)
        if procedure.can_create_new_revision():
            procedure.create_new_revision()
            return redirect('procedure_writer:view_procedure', procedure_id=procedure_id)
    raise PermissionDenied("A new procedure revision cannot be created at this time.")
    
# logic for handling if supposedly related objects are not in fact related.
def get_procedure_and_revision_or_raise_error(procedure_id, revision_id):
    procedure = get_object_or_404(Procedure, pk=procedure_id)
    revision = get_object_or_404(ProcedureRevision, pk=revision_id)
    if revision.procedure != procedure:
        raise BadRequest("The requested Procedure and Procedure Revision are not associated with each other.")
    return procedure, revision

# edit a procedure revision draft (add, remove, rearrange ProcedureElements).
def edit_procedure_revision(request, procedure_id, revision_id):
    procedure, revision = get_procedure_and_revision_or_raise_error(procedure_id, revision_id)
    context = {
        'procedure': procedure,
        'revision': revision,
    }
    return render(request, 'procedure_writer/procedure_revision_form.html', context)

# edit the metadata for an existing procedure revision draft.
def edit_procedure_revision_metadata(request, procedure_id, revision_id):
    procedure, revision = get_procedure_and_revision_or_raise_error(procedure_id, revision_id)
    form = ProcedureRevisionMetadataForm(request.POST or None, instance=revision)
    if form.is_valid():
        form.save()
        return redirect('procedure_writer:edit_procedure_revision', procedure_id=procedure.id, revision_id=revision.id)
    else:
        context = {
            'form': form,
            'page_title': "Edit Procedure Revision Metadata",
            'revision_title': revision,
        }
        return render(request, 'procedure_writer/procedure_revision_metadata_form.html', context)
    
# publish a revision
def publish_procedure_revision(request, procedure_id, revision_id):
    if request.method=='POST':
        procedure, revision = get_procedure_and_revision_or_raise_error(procedure_id, revision_id)
        if revision.can_be_published():
            revision.is_published = True
            revision.save()
            return redirect('procedure_writer:view_procedure', procedure_id=procedure.id)
    raise PermissionDenied("The revision cannot be published at this time.")

# un-publish a revision
def return_revision_to_draft(request, procedure_id, revision_id):
    if request.method=='POST':
        procedure, revision = get_procedure_and_revision_or_raise_error(procedure_id, revision_id)
        if revision.can_be_returned_to_draft():
            revision.is_published = False
            revision.save()
            return redirect('procedure_writer:view_procedure', procedure_id=procedure.id)
    raise PermissionDenied("The revision cannot be returned to draft at this time.")

# delete a revision - must be in draft mode
def delete_revision_draft(request, procedure_id, revision_id):
    procedure, revision = get_procedure_and_revision_or_raise_error(procedure_id, revision_id)
    if request.method == 'POST':
        revision.delete()
        return redirect('procedure_writer:view_procedure', procedure_id=procedure.id)
    else:
        context = {
            'revision': revision,
            'procedure': procedure,
        }
        return render(request, 'procedure_writer/procedure_revision_confirm_delete.html', context)