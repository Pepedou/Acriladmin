from dal import autocomplete
from django.forms import BaseInlineFormSet
from django.forms import ModelForm

from inventories.models import ProductTransferShipment, TransferredProduct


class TransferredProductInlineFormset(BaseInlineFormSet):
    """
    Formset used in the TransferredProductInlineAdmin. It's used to pass
    the request to each TransferredProductInlineForm.
    """

    def __init__(self, data=None, files=None, instance=None,
                 save_as_new=False, prefix=None, queryset=None, **kwargs):
        self.request = kwargs.pop('request')
        super(TransferredProductInlineFormset, self).__init__(data, files, instance, save_as_new, prefix, queryset,
                                                              **kwargs)

    def get_form_kwargs(self, index):
        form_kwargs = super(TransferredProductInlineFormset, self).get_form_kwargs(index)
        form_kwargs['request'] = self.request
        return form_kwargs


class TransferredProductInlineForm(ModelForm):
    """
    Custom form for adding or changing a transferred product.
    """

    class Meta:
        model = TransferredProduct
        fields = '__all__'
        widgets = {
            'product': autocomplete.ModelSelect2(url='product-autocomplete',
                                                 attrs={
                                                     'data-placeholder': 'Ejemplo: POL, 1.20, VERDE, cristal',
                                                     'data-minimum-input-length': 1,
                                                 })
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TransferredProductInlineForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(TransferredProductInlineForm, self).clean()

        if any(self.errors):
            return cleaned_data

        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        source_inventory = self.request.user.branch_office.productsinventory

        product_inventory_item = source_inventory.productinventoryitem_set.filter(product=product).first()

        if not product_inventory_item:
            self.add_error('product', 'El inventario {0} no cuenta con este producto.'.format(str(source_inventory)))
        elif product_inventory_item.quantity < quantity:
            self.add_error('quantity', 'El inventario {0} sólo cuenta con {1} unidades de este producto.'.format(
                str(source_inventory), product_inventory_item.quantity
            ))

        return cleaned_data


class AddOrChangeProductTransferShipmentForm(ModelForm):
    """
    Custom form for adding or changing a product transfer shipment.
    """

    class Meta:
        model = ProductTransferShipment
        fields = '__all__'
