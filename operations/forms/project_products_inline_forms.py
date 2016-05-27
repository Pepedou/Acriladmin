from dal import autocomplete
from django import forms
from django.conf import settings
from django.forms import ModelForm
from operations.models import ProjectProductsEntry


class ProjectProductsInLineForm(ModelForm):
    """
    Custom form for inlining products for a project.
    """
    product_price = forms.DecimalField(max_digits=10, decimal_places=2, label="Costo", initial=0.0,
                                       widget=forms.NumberInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = ProjectProductsEntry
        fields = "__all__"
        widgets = {
            'product': autocomplete.ModelSelect2(url='product-autocomplete',
                                                 attrs={
                                                     'data-placeholder': 'Ingrese un producto',
                                                     'data-minimum-input-length': 1,
                                                 })
        }

    class Media:
        js = (
            settings.JQUERY_LIB,
            'finances/scripts/productPrice.js',
            'operations/scripts/projectProductsInLineForm.js',
        )
