from dal import autocomplete
from django.forms import ModelForm
from inventories.models import ProductInventoryItem


class TabularInLineProductInventoryItemForm(ModelForm):
    """
    Custom form for adding or changing a product inventory item inline.
    """

    class Meta:
        model = ProductInventoryItem
        fields = '__all__'
        widgets = {
            'product': autocomplete.ModelSelect2(url='product-autocomplete',
                                                 attrs={
                                                     'data-placeholder': 'Ingrese un producto',
                                                     'data-minimum-input-length': 1,
                                                 })
        }
