from dal import autocomplete
from django.forms import ModelForm

from inventories.models import ProductTransfer, ProductsInventory


class AddOrChangeProductTransferForm(ModelForm):
    """
    Custom form for adding or changing a product transfer.
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddOrChangeProductTransferForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(AddOrChangeProductTransferForm, self).clean()
        source_branch = self.request.user.branch_office
        target_branch = cleaned_data.get('target_branch')
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity', self.instance.quantity)
        confirmed_quantity = cleaned_data.get('confirmed_quantity')
        is_confirmed = cleaned_data.get('is_confirmed')
        rejection_reason = cleaned_data.get('rejection_reason')

        if self.instance.id is not None:
            if is_confirmed and rejection_reason is not None:
                self.add_error('rejection_reason', 'No se puede rechazar un producto cuya recepción está confirmada. '
                                                   'Para hacerlo, deshabilite la confirmación o elimine el motivo de '
                                                   'rechazo.')
            elif not is_confirmed and rejection_reason is None:
                self.add_error('rejection_reason', 'Debe indicar un motivo para el rechazo de la transferencia.')

        if source_branch is not None and product is not None:
            try:
                source_inventory = source_branch.productsinventory
                inventory_item = source_inventory.productinventoryitem_set.filter(product=product).first()

                if inventory_item is None:
                    self.add_error('source_branch',
                                   'El inventario de la sucursal de origen no cuenta con ese producto.')

                if inventory_item.quantity < quantity:
                    self.add_error('source_branch',
                                   'El inventario de la sucursal de origen cuenta con {0} unidades de {1}.'.format(
                                       inventory_item.quantity,
                                       str(inventory_item.product))
                                   )
            except ProductsInventory.DoesNotExist:
                self.add_error('source_branch',
                               'La sucursal de origen no cuenta con un inventario de productos. Hay que agregar '
                               'uno antes de poder hacer una transferencia.')

        if target_branch is not None:
            try:
                target_branch.productsinventory
            except ProductsInventory.DoesNotExist:
                self.add_error('source_branch', 'La sucursal de destino no cuenta con un inventario de productos.')

        if quantity is not None and quantity == 0:
            self.add_error('quantity', "La cantidad a transferir debe ser mayor a 0.")

        if confirmed_quantity is not None and quantity is not None:
            if is_confirmed and confirmed_quantity > quantity:
                self.add_error('confirmed_quantity', 'La cantidad confirmada no puede ser mayor a la recibida.')

        return cleaned_data

    class Meta:
        model = ProductTransfer
        fields = '__all__'
        widgets = {
            'product': autocomplete.ModelSelect2(url='product-autocomplete',
                                                 attrs={
                                                     'data-placeholder': 'Ejemplo: POL, 1.20, VERDE, cristal',
                                                     'data-minimum-input-length': 1,
                                                 })
        }
