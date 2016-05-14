from dal import autocomplete
from django.forms import ModelForm
from finances.models import Sale


class AddOrChangeSaleForm(ModelForm):
    """
    Custom form for adding or changing a sale.
    """

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'product': autocomplete.ModelSelect2(url='product-autocomplete',
                                                 attrs={
                                                     'data-placeholder': 'Ingrese un producto',
                                                     'data-minimum-input-length': 1,
                                                 })
        }
