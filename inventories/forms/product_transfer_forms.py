from dal import autocomplete
from django.forms import ModelForm
from inventories.models import ProductTransfer


class AddOrChangeProductTransferForm(ModelForm):
    """
    Custom form for adding or changing a product transfer.
    """

    class Meta:
        model = ProductTransfer
        fields = '__all__'
        widgets = {
            'product': autocomplete.ModelSelect2(url='product-autocomplete',
                                                 attrs={
                                                     'data-placeholder': 'Ingrese un producto',
                                                     'data-minimum-input-length': 1,
                                                 })
        }
