import uuid

import django
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Sum, F, Q
from django.utils import timezone

from back_office.models import Client, Employee, Address, EmployeeGroup
from inventories.models import Product, Material, Product, Material, ProductsInventory, ProductInventoryItem
from operations.models import Service, Repair, Project


class Invoice(models.Model):
    """
    Commercial document issued by Acrilfrasa to a buyer related to a sale transaction
    and indicating the products, quantities and agreed prices for products or services
    provided.
    """

    STATE_VALID = 0
    STATE_GEN_BY_SALE = 1
    STATE_CANCELLED = 2
    INVOICE_STATES = (
        (STATE_VALID, 'Válida'),
        (STATE_GEN_BY_SALE, 'Venta'),
        (STATE_CANCELLED, 'Cancelada')
    )

    folio = models.CharField(max_length=50, primary_key=True, verbose_name='folio externo')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='total')
    file = models.FileField(blank=True, verbose_name="archivo")
    is_closed = models.BooleanField(default=False, verbose_name="cerrada")
    state = models.PositiveSmallIntegerField(choices=INVOICE_STATES, default=STATE_VALID, verbose_name='estado')

    class Meta:
        verbose_name = "factura"
        verbose_name_plural = "facturas"

    def __str__(self):
        return self.folio

    def has_been_paid(self):
        """
        Specifies if the invoice has been paid by the sum of all of the related transactions.
        :return: bool True if it has been paid, False otherwise.
        """
        aggregate = self.transaction_set.aggregate(sum=Sum(F('amount')))['sum']
        amount_paid = aggregate if aggregate is not None else 0

        return amount_paid >= self.total

    def save(self):
        related_transactions_sum = self.transaction_set.aggregate(sum=Sum(F('amount')))['sum']

        if related_transactions_sum is not None:
            if related_transactions_sum >= self.total:
                self.is_closed = True
            else:
                self.is_closed = False

        super(Invoice, self).save()

    def cancel(self):
        """
        Cancels the invoice, rendering it invalid.
        """
        self.state = Invoice.STATE_CANCELLED
        self.save()


class ProductPrice(models.Model):
    """
    Determines the price of a product.
    """
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True, verbose_name='producto')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='precio')
    authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT, blank=True, verbose_name='autorizado por',
                                      limit_choices_to=~Q(username='root'))

    class Meta:
        verbose_name = 'precio de producto'
        verbose_name_plural = 'precios de productos'

    def __str__(self):
        return "Precio - {0}: ${1}".format(self.product.sku, str(self.price))


class MaterialCost(models.Model):
    """
    Specifies the monetary cost of a material.
    """
    material = models.OneToOneField(Material, on_delete=models.CASCADE, verbose_name='material')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='costo')
    authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT, blank=True, verbose_name='autorizado por',
                                      limit_choices_to=~Q(username='root'))

    class Meta:
        verbose_name = 'costo de un material'
        verbose_name_plural = 'costos de materiales'

    def __str__(self):
        return str(self.cost)


class Transaction(models.Model):
    """
    Details a monetary transaction.
    """

    @property
    def folio(self):
        """
        Returns a folio using the Transaction's ID.
        :return: The folio as a string.
        """
        return "T{0}".format(str(self.id).zfill(9))

    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, verbose_name='factura')
    payed_by = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='pagado por')
    datetime = models.DateTimeField(default=django.utils.timezone.now, verbose_name='fecha y hora')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='monto')

    class Meta:
        verbose_name = 'transacción'
        verbose_name_plural = 'transacciones'

    def __str__(self):
        return self.folio


class RepairCost(models.Model):
    """
    The associated cost for a specific repair.
    """
    repair = models.ForeignKey(Repair, on_delete=models.PROTECT, verbose_name='reparación')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='costo')
    authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT, blank=True, verbose_name='autorizado por',
                                      limit_choices_to=~Q(username='root'))

    class Meta:
        verbose_name = 'costo de una reparación'
        verbose_name_plural = 'costos de reparaciones'

    def __str__(self):
        return "{0}: ${1}".format(self.repair, self.cost)


class Sale(models.Model):
    """
    The sale of a branch's product.
    """
    TYPE_COUNTER = 0
    TYPE_SHIPPING = 1
    SALE_TYPES = (
        (TYPE_COUNTER, "En mostrador"),
        (TYPE_SHIPPING, "Con entrega"),
    )

    PAYMENT_CASH = 0
    PAYMENT_TRANSFER = 1
    PAYMENT_ON_DELIVERY = 2
    PAYMENT_TYPES = (
        (PAYMENT_CASH, "Efectivo"),
        (PAYMENT_TRANSFER, "Transferencia"),
        (PAYMENT_ON_DELIVERY, "Contra entrega")
    )

    STATE_ACTIVE = 0
    STATE_CANCELLED = 1
    SALE_STATES = (
        (STATE_ACTIVE, 'Activa'),
        (STATE_CANCELLED, 'Cancelada')
    )

    @property
    def folio(self):
        """
        Returns a folio created base on the sale's ID.
        :return: The folio as a string.
        """
        return "V{0}".format(str(self.id).zfill(9))

    @property
    def total(self):
        return self.subtotal + self.shipping_and_handling - self.discount

    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='cliente')
    type = models.PositiveSmallIntegerField(verbose_name='tipo de venta', choices=SALE_TYPES, default=TYPE_COUNTER)
    state = models.PositiveSmallIntegerField(choices=SALE_STATES, blank=True, default=STATE_ACTIVE,
                                             verbose_name='estado')
    shipping_address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True,
                                         verbose_name='dirección de envío')
    payment_method = models.PositiveSmallIntegerField(choices=PAYMENT_TYPES, default=PAYMENT_CASH,
                                                      verbose_name='método de pago')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, verbose_name='factura',
                                limit_choices_to=~Q(state=Invoice.STATE_CANCELLED))
    transaction = models.OneToOneField(Transaction, on_delete=models.PROTECT, null=True, editable=False,
                                       verbose_name='transacción')
    inventory = models.ForeignKey(ProductsInventory, on_delete=models.PROTECT, editable=False,
                                  verbose_name='inventario')
    date = models.DateTimeField(auto_now_add=True, verbose_name='fecha de venta')
    subtotal = models.DecimalField(verbose_name='subtotal', max_digits=10, decimal_places=2, default=0)
    shipping_and_handling = models.DecimalField(verbose_name='manejo y envío', max_digits=10, decimal_places=2,
                                                default=0)
    discount = models.DecimalField(verbose_name='descuento', max_digits=10, decimal_places=2, default=0)
    driver = models.ForeignKey(Employee, null=True, blank=True,
                               limit_choices_to={'groups__name__contains': EmployeeGroup.DRIVER},
                               on_delete=models.PROTECT,
                               verbose_name='chofer')

    class Meta:
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'

    def __str__(self):
        return self.folio

    def cancel(self):
        """
        Cancels the Sale, rendering it invalid. It restores the given quantity of the Sale's Product
        to its corresponding inventory. If the Sale was the only Sale for its Invoice, the Invoice is
        also cancelled.
        """
        if self.state == Sale.STATE_CANCELLED:
            return

        self.state = Sale.STATE_CANCELLED

        product_inventory_item_set = self.inventory.productinventoryitem_set.filter(
            product__in=[x.product for x in self.saleproductitem_set.all()])

        with transaction.atomic():
            item_tuples = [(inv_item, sale_item,)
                           for inv_item in product_inventory_item_set
                           for sale_item in self.saleproductitem_set.all()
                           if inv_item.product == sale_item.product]

            for inv_item, sale_item in item_tuples:
                inv_item.quantity += sale_item.quantity
                inv_item.save()

            self.inventory.save()
            self.save()

            if self.invoice is not None and self.invoice.sale_set.count() == 1:
                self.invoice.cancel()


class SaleProductItem(models.Model):
    """
    A product and the amount of that product that belongs
    to a Sale.
    """
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='producto')
    quantity = models.PositiveIntegerField(default=1, verbose_name='cantidad')
    special_length = models.DecimalField(max_digits=6, decimal_places=2, default=0,
                                         verbose_name='longitud especial (m)')
    special_width = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='anchura especial (m)')
    special_thickness = models.DecimalField(max_digits=6, decimal_places=2, default=0,
                                            verbose_name='grosor especial (mm)')
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name='venta')

    class Meta:
        verbose_name = 'producto de la venta'
        verbose_name_plural = 'productos de la venta'

    def __str__(self):
        return "{0}: {1}".format(str(self.product), str(self.quantity))
