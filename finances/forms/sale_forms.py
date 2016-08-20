from dal import autocomplete
from django.core.exceptions import ValidationError
from django.forms import ModelForm, BaseInlineFormSet

from finances.models import Sale, SaleProductItem, ProductPrice


class SaleProductItemInlineFormSet(BaseInlineFormSet):
    """
    Overrides BaseInlineFormSet to receive the request and pass it
    to the SaleProductItemInlineForms as an extra kwarg in the
    constructor.
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SaleProductItemInlineFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['request'] = self.request
        return super(SaleProductItemInlineFormSet, self)._construct_form(i, **kwargs)


class SaleProductItemInlineForm(ModelForm):
    """
    Custom form for the Sale Product Item Inline used by the
    Sale Admin form.
    """

    class Meta:
        model = SaleProductItem
        fields = "__all__"
        widgets = {
            'product': autocomplete.ModelSelect2(url='product-autocomplete',
                                                 attrs={
                                                     'data-placeholder': 'Ejemplo: POL, 1.20, VERDE, cristal',
                                                     'data-minimum-input-length': 1,
                                                 }),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SaleProductItemInlineForm, self).__init__(*args, **kwargs)

    def clean(self):
        # TODO: Divide and document
        cleaned_data = super(SaleProductItemInlineForm, self).clean()
        inventory = self.request.user.branch_office.productsinventory
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        special_length = cleaned_data.get('special_length')
        special_width = cleaned_data.get('special_width')
        special_thickness = cleaned_data.get('special_thickness')

        product_inventory_item = inventory.productinventoryitem_set.filter(product=product).first()

        if product_inventory_item is None:
            raise ValidationError({'product': 'El inventario elegido no cuenta con este producto.'})

        if product_inventory_item.quantity < quantity:
            raise ValidationError({
                'product':
                    'El inventario elegido sólo cuenta con {0}/{1} unidades de este producto.'.format(
                        product_inventory_item.quantity,
                        quantity
                    )})

        if ProductPrice.objects.filter(product=product).first() is None:
            raise ValidationError({
                'product': 'El producto no cuenta con un precio. Debe asignar un precio a este producto antes '
                           'de poder hacer una venta.'
            })

        if special_length > 0 or special_width > 0 or special_thickness > 0:
            errors = {}
            if product.length < special_length:
                errors.update({
                    'special_length': 'La longitud especial solicitada es mayor que la '
                                      'longitud del producto: {0}/{1}'.format(special_length, product.length)
                })

            if product.width < special_width:
                errors.update({
                    'special_width': 'La anchura especial solicitada es mayor que la '
                                     'anchura del producto: {0}/{1}'.format(special_width, product.width)
                })

            if product.thickness < special_thickness:
                errors.update({
                    'special_thickness': 'El grosor especial solicitado es mayor que el '
                                         'grosor del producto: {0}/{1}'.format(special_thickness, product.thickness)
                })

            if len(errors):
                raise ValidationError(errors)


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
                                                }),
            'invoice': autocomplete.ModelSelect2(url='invoice-autocomplete',
                                                 attrs={
                                                     'data-placeholder':
                                                         'Ingrese el folio de una factura...',
                                                     'data-minimum-input-length': 1
                                                 })
        }

    class Media:
        js = [
            "finances/scripts/addOrChangeSaleForm.js",
        ]
