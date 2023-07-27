from django.db import models
from django.dispatch import receiver

# An instance of the Procedure model represents 
# the broad goal of a given real-life procedure. 
# They are (will be) related to a work object 
# category and to a project. Actual implementations 
# of the procedure are stored in ProcedureRevisions.
class Procedure(models.Model):
    # TODO: think about what level of uniqueness is appropriate
    title = models.CharField(max_length=200, unique=True)

    # for the purposes of data safety, Procedures CANNOT be
    # deleted if there are any filled out travelers or data
    # fields that belong to it.

    def __str__(self):
        return self.title

    def next_revision_number(self):
        used_numbers = [r.revision_number for r in self.revisions.all()]
        if used_numbers:
            return max(used_numbers)
        else:
            return 0
    
    # TODO: if not first revision, copy the previous one
    def create_new_revision(self):
        revision = ProcedureRevision(procedure = self, revision_number = self.next_revision_number())
        revision.save()
        return revision

    # most of the time, when we save a Procedure, 
    # we will want to ensure that there is at least 1 ProcedureRevision.
    # This function is here (and not in a post_save signal hook) so that it 
    # doesn't get called when using the admin interface.
    def ensure_revision_present(self):
        if not self.revisions.exists():
            self.create_new_revision()
        else:
            pass

    # TODO: delete() function. Requires logic to check for existing Travelers



# DataFields belong to procedures in a many-to-one relationship. They have names that describe what data is expected to be entered in a given traveler. The names are unique with respect to sibling DataFields within the same parent Procedure. DataFields have a field type, selected from a list. They have a unit which is strongly recommended to be defined if the field type is numeric.
class DataField(models.Model):
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, related_name='data_fields')
    name = models.CharField(max_length = 100)
    FIELD_TYPE_CHOICES = [
        ("passfail", "Pass/Fail"),
        ("truefalse", "True/False"),
        ("float", "Floating point decimal"),
        ("int", "Integer"),
        ("char", "Short text (char)"),
        ("text", "Long text"),
        ("date", "Date"),
        ("time", "Time"),
        #("personnel", "Personnel/inspector/approver"),
        #("file", "File upload"),
        #("workobject", "Work object"),
    ]
    field_type = models.CharField(choices=FIELD_TYPE_CHOICES, default="char")
    unit = models.CharField(max_length=100, blank=True)

    class Meta:
        constraints = [
            # field name must be unique within the procedure
            models.UniqueConstraint(fields=["procedure","name"], name="unique_name_within_procedure", violation_error_message="Field name already used within the procedure.")
        ]



# ProcedureRevisions are implementations of Procedures.
# Each procedure has at least one. Travelers, when they
# are filled out, are done so with respect to one revision
# of the procedure. Child elements belonging to a 
# ProcedureRevision instance form a tree that can be 
# traversed to yield the traveler form.
class ProcedureRevision(models.Model):
    procedure = models.ForeignKey(
        Procedure, 
        on_delete=models.CASCADE, 
        related_name='revisions'
        )
    revision_number = models.PositiveIntegerField(default=0) # TODO: better default
    reference_document_title = models.CharField(
        max_length=200, 
        blank=True, 
        help_text="Please include document revision number (if applicable)."
        )
    reference_document_URL = models.URLField(blank=True)
    is_published = models.BooleanField(
        default=False, 
        verbose_name="Publish revision",
        help_text="If the box is unchecked, the revision is in draft mode.",
        )
    # revision_notes = models.TextField() # TODO add this with markdown-compatible field

    def __str__(self):
        return self.procedure.__str__() + f" (rev { self.revision_number })"

    class Meta:
        constraints = [
            # revision number must be unique within the procedure
            models.UniqueConstraint(fields=["procedure","revision_number"], name="unique_revision_number_within_procedure", violation_error_message="Revision number already used.")
        ]

