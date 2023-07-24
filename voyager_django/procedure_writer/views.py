from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from .models import Procedure
from .forms import ProcedureForm


def index(request):
    procedure_list = Procedure.objects.order_by('title')
    return render(request, 'procedure_writer/index.html', {'procedure_list': procedure_list})

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
            procedure.ensure_revision_present()
            # TODO: return a redirect to the procedure revision form
            return HttpResponseRedirect(reverse('procedure_writer:index'))

