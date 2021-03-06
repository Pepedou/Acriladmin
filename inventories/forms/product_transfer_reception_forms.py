import logging

from dal import autocomplete
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import BaseInlineFormSet
from django.forms import ModelForm

from inventories.models import ReceivedProduct, ProductTransferReception, ProductTransferShipment

db_logger = logging.getLogger('db')


class ReceivedProductInlineFormset(BaseInlineFormSet):
    """
    Formset used in the ReceivedProductInlineAdmin. It's used to pass
    the request to each ReceivedProductInlineForm.
    """

    def __init__(self, data=None, files=None, instance=None,
                 save_as_new=False, prefix=None, queryset=None, **kwargs):
        self.request = kwargs.pop('request')
        super(ReceivedProductInlineFormset, self).__init__(data, files, instance, save_as_new, prefix, queryset,
                                                           **kwargs)

    def get_form_kwargs(self, index):
        form_kwargs = super(ReceivedProductInlineFormset, self).get_form_kwargs(index)
        form_kwargs['request'] = self.request
        return form_kwargs


class ReceivedProductInlineForm(ModelForm):
    """
    Custom form for adding or changing a transferred product.
    """

    class Meta:
        model = ReceivedProduct
        fields = '__all__'
        widgets = {
            'product': autocomplete.ModelSelect2(url='product-autocomplete',
                                                 attrs={
                                                     'data-placeholder': 'Ejemplo: POL, 1.20, VERDE, cristal',
                                                     'data-minimum-input-length': 1,
                                                 })
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ReceivedProductInlineForm, self).__init__(*args, **kwargs)

    def clean(self):
        try:
            cleaned_data = super(ReceivedProductInlineForm, self).clean()

            if any(self.errors):
                return cleaned_data

            received_quantity = cleaned_data.get('received_quantity')
            accepted_quantity = cleaned_data.get('accepted_quantity')
            rejection_reason = cleaned_data.get('rejection_reason')

            if accepted_quantity > received_quantity:
                self.add_error('accepted_quantity', 'No se puede aceptar una cantidad superior '
                                                    'a la recibida.')

            if rejection_reason is not None and received_quantity == accepted_quantity:
                self.add_error('rejection_reason', 'Si la cantidad recibida es igual a la cantidad aceptada, '
                                                   'no debe haber un motivo de rechazo.')

            if accepted_quantity < received_quantity and rejection_reason is None:
                self.add_error('rejection_reason', 'Debe especificar un motivo de rechazo si no va a '
                                                   'aceptar toda la cantidad recibida.')

            return cleaned_data
        except Exception as e:
            db_logger.exception(e)
            raise


class AddOrChangeProductTransferReceptionForm(ModelForm):
    """
    Custom form for adding or changing a product transfer reception.
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(AddOrChangeProductTransferReceptionForm, self).__init__(*args, **kwargs)
        if 'product_transfer_shipment' in self.fields:
            self.fields['product_transfer_shipment'].queryset = ProductTransferShipment.objects.filter(
                target_branch=self.request.user.branch_office, status=ProductTransferShipment.STATUS_CONFIRMED)

    class Meta:
        model = ProductTransferReception
        fields = '__all__'

    def clean_product_transfer_shipment(self):
        try:
            product_transfer_shipment = self.cleaned_data.get('product_transfer_shipment')
            receiving_branch = self.request.user.branch_office

            if not product_transfer_shipment:
                raise ValidationError('No se encuentra la transferencia de producto.')

            if receiving_branch != product_transfer_shipment.target_branch:
                self.add_error('product_transfer_shipment', 'Esta transferencia está dirigida a {0}, no a {1}.'.format(
                    str(product_transfer_shipment.target_branch), str(receiving_branch)
                ))

            total_transferred_products = product_transfer_shipment.total_transferred_products
            pending_and_confirmed_products = \
                product_transfer_shipment.get_total_received_products_by_target_branch_with_filter(
                    Q(status=ProductTransferReception.STATUS_PENDING) | Q(
                        status=ProductTransferReception.STATUS_CONFIRMED))

            if total_transferred_products >= pending_and_confirmed_products:
                raise ValidationError('No se puede agregar otra recepción a esta transferencia ya que, '
                                      'entre las recepciones confirmadas y pendientes, ya se han recibido todos los '
                                      'productos de la transferencia.')

            return product_transfer_shipment
        except Exception as e:
            db_logger.exception(e)
            raise
