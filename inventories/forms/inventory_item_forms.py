from dal import autocomplete
from django.forms import ModelForm
from inventories.models import ProductInventoryItem, MaterialInventoryItem, ConsumableInventoryItem, \
    DurableGoodInventoryItem


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
                                                     'data-placeholder': 'Ejemplo: POL, 1.20, VERDE, cristal',
                                                     'data-minimum-input-length': 1,
                                                 })
        }


class TabularInLineMaterialInventoryItemForm(ModelForm):
    """
    Custom form for adding or changing a material inventory item inline.
    """

    class Meta:
        model = MaterialInventoryItem
        fields = '__all__'
        widgets = {
            'material': autocomplete.ModelSelect2(url='material-autocomplete',
                                                  attrs={
                                                      'data-placeholder': 'Ingrese un material',
                                                      'data-minimum-input-length': 1,
                                                  })
        }


class TabularInLineConsumableInventoryItemForm(ModelForm):
    """
    Custom form for adding or changing a consumable inventory item inline.
    """

    class Meta:
        model = ConsumableInventoryItem
        fields = '__all__'
        widgets = {
            'consumable': autocomplete.ModelSelect2(url='consumable-autocomplete',
                                                    attrs={
                                                        'data-placeholder': 'Ingrese un consumible',
                                                        'data-minimum-input-length': 1,
                                                    })
        }


class TabularInLineDurableGoodInventoryItemForm(ModelForm):
    """
    Custom form for adding or changing a durable good inventory item inline.
    """

    class Meta:
        model = DurableGoodInventoryItem
        fields = '__all__'
        widgets = {
            'durable_good': autocomplete.ModelSelect2(url='durablegood-autocomplete',
                                                      attrs={
                                                          'data-placeholder': 'Ingrese un activo',
                                                          'data-minimum-input-length': 1,
                                                      })
        }
