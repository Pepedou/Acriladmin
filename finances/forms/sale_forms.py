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
                                                     'data-placeholder': 'Ejemplo: POL, 1.20, VERDE, cristal',
                                                     'data-minimum-input-length': 1,
                                                 }),
            'shipping_address': autocomplete.ModelSelect2(url='address-autocomplete',
                                                          attrs={
                                                              'data-placeholder': 'Ingrese una calle, ciudad, '
                                                                                  'región o país...',
                                                              'data-minimum-input-length': 3,
                                                          }),
            'client': autocomplete.ModelSelect2(url='client-autocomplete',
                                                attrs={
                                                    'data-placeholder': 'Ingrese el nombre de un cliente...',
                                                    'data-minimum-input-length': 1
                                                })
        }
