from django.conf import settings
from django.forms import ModelForm
from operations.models import Project


class AddOrChangeProjectForm(ModelForm):
    """
    Custom form for adding or changing a project.
    """

    class Meta:
        model = Project
        fields = "__all__"

    class Media:
        js = (
            settings.JQUERY_LIB,
            'operations/scripts/projectEditForm.js',
        )
