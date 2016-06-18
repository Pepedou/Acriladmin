import django

from back_office.models import Client, Employee, Address
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Sum, F, Q
from inventories.models import Product, Material, Product, Material, ProductsInventory
from operations.models import Service, Repair, Project


class Invoice(models.Model):
    """
    Commercial document issued by Acrilfrasa to a buyer related to a sale transaction
    and indicating the products, quantities and agreed prices for products or services
    provided.
    """
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='total')
    file = models.FileField(blank=True, verbose_name="archivo")
    is_closed = models.BooleanField(default=False, verbose_name="cerrada")

    class Meta:
        verbose_name = "factura"
        verbose_name_plural = "facturas"

    def __str__(self):
        return str(self.id).zfill(9)

    def has_been_paid(self):
        """
        Specifies if the invoice has been paid by the sum of all of the related transactions.
        :return: bool True if it has been paid, False otherwise.
        """
        amount_paid = Transaction.objects.filter(invoice_id=self.id).aggregate(sum=Sum(F('amount')))

        return amount_paid['sum'] >= self.total

    def save(self):
        related_transactions_sum = Transaction.objects.filter(invoice_id=self.id).aggregate(
            sum=Sum(F('amount')))['sum']

        if related_transactions_sum is not None:
            if related_transactions_sum >= self.total:
                self.is_closed = True
            else:
                self.is_closed = False

        super(Invoice, self).save()


class ProductPrice(models.Model):
    """
    Determines the price of a product.
    """
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name='producto')
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
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, verbose_name='factura')
    payed_by = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='pagado por')
    datetime = models.DateTimeField(default=django.utils.timezone.now, verbose_name='fecha y hora')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='monto')

    class Meta:
        verbose_name = 'transacción'
        verbose_name_plural = 'transacciones'

    def __str__(self):
        return "{0}: ${1}".format(self.datetime.date(), self.amount)


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

    @property
    def total(self):
        return self.subtotal + self.shipping_and_handling - self.discount

    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='cliente')
    type = models.PositiveSmallIntegerField(verbose_name='tipo de venta', choices=SALE_TYPES, default=TYPE_COUNTER)
    shipping_address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True,
                                         verbose_name='dirección de envío')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='producto')
    quantity = models.PositiveIntegerField(default=1, verbose_name='cantidad')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True, verbose_name='factura')
    inventory = models.ForeignKey(ProductsInventory, on_delete=models.PROTECT, verbose_name='inventario')
    date = models.DateTimeField(auto_now_add=True, verbose_name='fecha de venta')
    date = models.DateField(verbose_name='fecha', default=django.utils.timezone.now)
    subtotal = models.DecimalField(verbose_name='subtotal', max_digits=10, decimal_places=2, default=0.00)
    shipping_and_handling = models.DecimalField(verbose_name='manejo y envío', max_digits=10, decimal_places=2,
                                                default=0.00)
    discount = models.DecimalField(verbose_name='descuento', max_digits=10, decimal_places=2, default=0.00)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.0, verbose_name='monto')

    class Meta:
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'

    def __str__(self):
        return "{0} - {1} ({2})".format(self.date.strftime("%x"), str(self.product), str(self.quantity))

    def clean(self):
        super(Sale, self).clean()

        if self.id is not None:
            return

        if self.quantity == 0:
            raise ValidationError({
                'quantity': 'La cantidad debe ser mayor a 0.'
            })

        product_inventory_item_set = self.inventory.productinventoryitem_set.filter(product=self.product)
        product_price_set = ProductPrice.objects.filter(product=self.product)

        if product_inventory_item_set.count() == 0:
            raise ValidationError({
                'inventory': 'El inventario no cuenta con el producto elegido.'
            })

        product_inventory_item = product_inventory_item_set[0]

        if product_inventory_item.quantity < self.quantity:
            raise ValidationError({
                'quantity': 'El inventario sólo cuenta con {0} unidades del producto elegido.'.format(
                    product_inventory_item.quantity)
            })

        if product_price_set.count() == 0:
            raise ValidationError({
                'product': 'A este produto no se le ha asignado un precio. No se puede generar'
                           ' la venta hasta que tenga un precio.'
            })

    def save(self):
        if self.id is not None:
            super(Sale, self).save()
            return

        product_inventory_item = self.inventory.productinventoryitem_set.filter(product=self.product)[0]

        product_inventory_item.quantity -= self.quantity

        product_price = ProductPrice.objects.filter(product=self.product)[0]

        self.amount = product_price.price * self.quantity
        # TODO: Check if a Transaction is needed for an Invoice to be considered closed.
        self.invoice = Invoice(total=self.amount, is_closed=True)

        with transaction.atomic():
            self.invoice.save()
            product_inventory_item.save()
            super(Sale, self).save()
