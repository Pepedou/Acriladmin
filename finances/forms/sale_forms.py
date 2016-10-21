from dal import autocomplete
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import ModelForm, BaseInlineFormSet

from finances.models import Sale, SaleProductItem, ProductPrice, Invoice, Transaction
from inventories.models import Product, ProductInventoryItem
from utils.product_helpers import ScrapsToProductsConverter


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
        self.original_product = None
        self.subproduct = None
        self.scraps_products = []
        self.has_subproduct = False
        super(SaleProductItemInlineForm, self).__init__(*args, **kwargs)

    def clean(self):
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

        return cleaned_data

    def save(self, commit=True):
        if self.instance.pk is not None:
            return super(SaleProductItemInlineForm, self).save(commit)

        self.original_product = self.instance.product
        self.has_subproduct = self.instance.special_length > 0 or \
                              self.instance.special_width > 0 or \
                              self.instance.special_thickness > 0

        if self.has_subproduct:
            self._create_subproduct()
            self._create_scraps_products()
            sale_product_price = self._get_sale_product_price()
            self.instance.product = self.subproduct
        else:
            sale_product_price = ProductPrice.objects.filter(product=self.instance.product).first()

        self._assign_financial_information(sale_product_price)

        return super(SaleProductItemInlineForm, self).save(commit)

    def _create_subproduct(self):
        """
        Creates a new Product based on the Sale's special measurements.
        The new Product is subtracted from the original Product's surface.
        """
        self.subproduct, _ = Product.objects.get_or_create(
            description=self.original_product.description + " [RECORTADO A {:.2f}*{:.2f}]".format(
                self.instance.special_width, self.instance.special_length
            ),
            search_description=self.original_product.search_description + " [RECORTADO A {:.2f}X{:.2f}]".format(
                self.instance.special_width, self.instance.special_length
            ),
            line=self.original_product.line,
            engraving=self.original_product.engraving,
            color=self.original_product.color,
            length=self.instance.special_length,
            width=self.instance.special_width,
            thickness=self.instance.special_thickness,
            is_composite=self.original_product.is_composite,
            defaults={
                'sku': self.original_product.sku + "_{}*{}_PED".format(self.instance.special_width,
                                                                       self.instance.special_length)
            }
        )

    def _create_scraps_products(self):
        """
        Creates new Products from the original Product's scraps.
        The way it does this is by calculating the remaining surface after
        the subproduct has been subtracted from the original and dividing
        it into new products. For each scraps Product, a Product Price
        matching the original Product's price is created.
        """
        scraps_converter = ScrapsToProductsConverter(
            self.instance.special_length, self.instance.special_width, self.instance.special_thickness,
            self.original_product
        )

        scraps_params = scraps_converter.get_products_params_from_scraps()

        for params in scraps_params:
            scraps_product, item_created = Product.objects.update_or_create(
                sku=params['sku'],
                defaults=params
            )

            original_product_price = ProductPrice.objects.filter(product=self.original_product).first()

            if item_created:
                ProductPrice.objects.create(
                    product=scraps_product,
                    price=original_product_price.price,
                    authorized_by=self.request.user
                )

            self.scraps_products.append(scraps_product)

    def _get_sale_product_price(self):
        """
        Obtains the appropraite Product Price for the sale.
        :return: The Sale's Product Price.
        """
        original_product_price = ProductPrice.objects.filter(product=self.original_product).first()

        sale_product_price, _ = ProductPrice.objects.get_or_create(
            product=self.subproduct,
            defaults={
                'price': original_product_price.price,
                'authorized_by': self.request.user
            })

        return sale_product_price

    def _assign_financial_information(self, sale_product_price):
        """
        Calculates the Sale's subtotal based on the sale product's price
        and the quantity requested. It also updates the Invoice's total
        and creates a transaction, if the conditions are appropriate.
        :param sale_product_price: The product's price.
        """
        item_charges = self.instance.quantity * sale_product_price.price

        self.instance.sale.subtotal += item_charges

        if self.instance.sale.invoice.state == Invoice.STATE_GEN_BY_SALE:
            self.instance.sale.invoice.total += self.instance.sale.total

        if self.instance.sale.payment_method is not Sale.PAYMENT_ON_DELIVERY:
            self.instance.sale.transaction.amount += item_charges

    def _save_m2m(self):
        """
        Saves entities related to the Sale.
        """

        with transaction.atomic():
            self.instance.sale.save()
            self.instance.sale.invoice.save()

            if self.instance.sale.transaction is not None:
                self.instance.sale.transaction.save()

            self._update_product_inventory_item()
            self._update_scraps_products_inventory_items()

        super(SaleProductItemInlineForm, self)._save_m2m()

    def _update_product_inventory_item(self):
        """
        The amount of product requested in the Sale is removed
        from the associated inventory.
        """
        products_inventory = self.request.user.branch_office.productsinventory
        product_inventory_item = products_inventory.productinventoryitem_set.filter(
            product=self.original_product).first()

        product_inventory_item.quantity -= self.instance.quantity
        product_inventory_item.save()

    def _update_scraps_products_inventory_items(self):
        """
        For each scraps product that was created as a consequence
        of the subproduct's creation, an inventory item is created
        or updated. It adds the scraps product to the associated
        products inventory.
        """
        for scraps_product in self.scraps_products:
            inventory_item, _ = ProductInventoryItem.objects.get_or_create(
                product=scraps_product,
                inventory=self.request.user.branch_office.productsinventory,
            )

            inventory_item.quantity += 1
            inventory_item.save()


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

    def clean(self):
        cleaned_data = super(AddOrChangeSaleForm, self).clean()
        sale_type = cleaned_data.get('type')
        payment_method = cleaned_data.get('payment_method')
        driver = cleaned_data.get('driver')

        if sale_type == Sale.TYPE_COUNTER and payment_method == Sale.PAYMENT_ON_DELIVERY:
            self.add_error('payment_method',
                           'No se puede elegir pago "Contra entrega" si el tipo de venta es "Mostrador". '
                           'Para esto elija tipo de venta "Con entrega".')
        elif sale_type == Sale.TYPE_SHIPPING and driver is None:
            self.add_error('driver', "Si el tipo de venta es Con entrega, se debe especificar un conductor.")

        return cleaned_data

    def save(self, commit=True):
        if self.instance.payment_method is not Sale.PAYMENT_ON_DELIVERY:
            self.instance.transaction = Transaction.objects.create(invoice=self.instance.invoice,
                                                                   payed_by=self.instance.client)
            self.instance.invoice.is_closed = True
            self.instance.invoice.transaction_set.add(self.instance.transaction)

        return super(AddOrChangeSaleForm, self).save(commit)
