from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import ModelForm

from inventories.models import ProductEntry, PurchaseOrder


class AddOrChangeProductEntryForm(ModelForm):
    """
    Custom form for adding or changing a product entry.
    """

    class Meta:
        model = ProductEntry
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddOrChangeProductEntryForm, self).__init__(*args, **kwargs)
        if 'purchase_order' in self.fields:
            self.fields['purchase_order'].queryset = PurchaseOrder.objects.filter(status=PurchaseOrder.STATUS_CONFIRMED)

    def clean_purchase_order(self):
        purchase_order = self.cleaned_data.get('purchase_order')

        if purchase_order is None:
            return purchase_order

        total_purchased_products = purchase_order.total_purchased_products
        pending_and_confirmed_products = \
            purchase_order.get_total_entered_products_with_filter(
                Q(status=ProductEntry.STATUS_PENDING) | Q(
                    status=ProductEntry.STATUS_CONFIRMED))

        if total_purchased_products <= pending_and_confirmed_products:
            raise ValidationError('No se puede agregar otro ingreso de producto a esta orden de compra ya que, '
                                  'entre los ingresos confirmados y pendientes, ya se han recibido todos los '
                                  'productos de la compra.')

        return purchase_order
