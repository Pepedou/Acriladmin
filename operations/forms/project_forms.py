from django import forms
from django.conf import settings
from django.forms import ModelForm
from operations.models import Project


class AddOrChangeProjectForm(ModelForm):
    """
    Custom form for adding or changing a project.
    """
    amount_paid = forms.IntegerField(label='Cantidad pagada', initial=0.0,
                                     widget=forms.NumberInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Project
        fields = "__all__"

    class Media:
        js = (
            settings.JQUERY_LIB,
            'operations/scripts/projectEditForm.js',
        )