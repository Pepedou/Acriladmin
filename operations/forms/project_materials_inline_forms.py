from django import forms
from django.conf import settings
from django.forms import ModelForm
from operations.models import ProjectMaterialsEntry


class ProjectMaterialsInLineForm(ModelForm):
    """
    Custom form for inlining materials for a project.
    """
    material_cost = forms.DecimalField(max_digits=10, decimal_places=2, label="Costo", required=False,
                                       widget=forms.NumberInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = ProjectMaterialsEntry
        fields = "__all__"

    class Media:
        js = (
            settings.JQUERY_LIB,
            'finances/scripts/materialCost.js',
            'operations/scripts/projectMaterialsInLineForm.js',
        )
