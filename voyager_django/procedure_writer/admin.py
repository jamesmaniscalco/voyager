from django.contrib import admin

from .models import Procedure, DataField, ProcedureRevision

admin.site.register(Procedure)
admin.site.register(ProcedureRevision)
admin.site.register(DataField)
