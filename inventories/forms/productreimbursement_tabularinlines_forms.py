from dal import autocomplete
from django.forms import ModelForm
from inventories.models import ReturnedProduct


class AddOrChangeReturnedProductTabularInlineForm(ModelForm):
    """
    Custom form for adding or changing a returned product.
    """

    class Meta:
        model = ReturnedProduct
        fields = '__all__'
        widgets = {
            'product': autocomplete.ModelSelect2(url='product-autocomplete',
                                                 attrs={
                                                     'data-placeholder': 'Ejemplo: POL, 1.20, VERDE, cristal',
                                                     'data-minimum-input-length': 1,
                                                 })
        }
