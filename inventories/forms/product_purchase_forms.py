from dal import autocomplete
from django.forms import ModelForm

from inventories.models import PurchasedProduct


class PurchasedProductInlineForm(ModelForm):
    """
    Form for the PurchasedProductInline.
    """

    class Meta:
        model = PurchasedProduct
        fields = '__all__'
        widgets = {
            'product': autocomplete.ModelSelect2(url='product-autocomplete',
                                                 attrs={
                                                     'data-placeholder': 'Ejemplo: POL, 1.20, VERDE, cristal',
                                                     'data-minimum-input-length': 1,
                                                 })
        }
