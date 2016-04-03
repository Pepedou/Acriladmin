import django

from back_office.models import Client, Employee
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, F
from inventories.models import Product, Material, ProductDefinition, MaterialDefinition
from operations.models import Service, Repair, Project


class Order(models.Model):
    """
    An order of products made by a client.
    """
    PLACED = 0
    IN_PROGRESS = 1
    COMPLETE = 2
    DELIVERED = 3
    CANCELLED = 4
    RETURNED = 5
    STATUS_CHOICES = (
        (PLACED, "Solicitada"),
        (IN_PROGRESS, "En progreso"),
        (COMPLETE, "Completa"),
        (DELIVERED, "Entregada"),
        (CANCELLED, "Cancelada"),
        (RETURNED, "Devuelta"),
    )

    PROJECT = 0
    PRODUCTS = 1
    SERVICES = 2
    PRODUCTS_AND_SERVICES = 3
    ALL = 4
    TARGET_CHOICES = (
        (PROJECT, "Proyecto"),
        (PRODUCTS, "Productos"),
        (SERVICES, "Servicios"),
        (PRODUCTS_AND_SERVICES, "Productos y servicios"),
        (ALL, "Todos"),
    )

    @property
    def total(self):
        return self.subtotal + self.shipping_and_handling - self.discount

    status = models.PositiveSmallIntegerField(verbose_name='estado', default=PLACED, choices=STATUS_CHOICES)
    target = models.PositiveSmallIntegerField(verbose_name='entregable', choices=TARGET_CHOICES)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='cliente')
    date = models.DateField(verbose_name='fecha', default=django.utils.timezone.now)
    subtotal = models.DecimalField(verbose_name='subtotal', max_digits=10, decimal_places=2, default=0.00)
    shipping_and_handling = models.DecimalField(verbose_name='manejo y envío', max_digits=10, decimal_places=2,
                                                default=0.00)
    discount = models.DecimalField(verbose_name='descuento', max_digits=10, decimal_places=2, default=0.00)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, verbose_name='proyecto')

    class Meta:
        verbose_name = 'orden'
        verbose_name_plural = 'órdenes'

    def __str__(self):
        return str(self.id).zfill(9)


class OrderProducts(models.Model):
    """
    An entry that relates a quantity of a certain product with an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='orden')
    product = models.ForeignKey(ProductDefinition, on_delete=models.PROTECT, verbose_name='producto')
    quantity = models.PositiveIntegerField(verbose_name='cantidad', default=1)

    class Meta:
        verbose_name = 'productos de una orden'
        verbose_name_plural = 'productos de órdenes'

    def __str__(self):
        return "{0} - {1}".format(self.order, self.product)


class OrderServices(models.Model):
    """
    An entry that relates a service with an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='orden')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='servicio')

    class Meta:
        verbose_name = 'servicios de una orden'
        verbose_name_plural = 'servicios de órdenes'

    def __str__(self):
        return "{0} - {1}".format(self.order, self.service)


class Invoice(models.Model):
    """
    Commercial document issued by Acrilfrasa to a buyer related to a sale transaction
    and indicating the products, quantities and agreed prices for products or services
    provided.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="orden")
    file = models.FileField(blank=True, verbose_name="archivo")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='total')
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


class ProductInvoice(models.Model):
    """
    An entry that relates a concrete product with an invoice.
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, verbose_name="factura")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="producto")

    class Meta:
        verbose_name = "factura de producto"
        verbose_name_plural = "facturas de producto"

    def __str__(self):
        return "{0} - {1}".format(self.invoice, self.product)


class ProductPrice(models.Model):
    """
    Determines the price of a product.
    """
    product = models.OneToOneField(ProductDefinition, on_delete=models.CASCADE, verbose_name='producto')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='precio')
    authorized_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, verbose_name='autorizado por')

    class Meta:
        verbose_name = 'precio de producto'
        verbose_name_plural = 'precios de productos'

    def __str__(self):
        return str(self.price)


class MaterialCost(models.Model):
    """
    Specifies the monetary cost of a material.
    """
    material = models.OneToOneField(MaterialDefinition, on_delete=models.CASCADE, verbose_name='material')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='costo')
    authorized_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, verbose_name='autorizado por')

    class Meta:
        verbose_name = 'costo de un material'
        verbose_name_plural = 'costos de materiales'

    def __str__(self):
        return str(self.cost)


class ServiceInvoice(models.Model):
    """
    An entry that relates a service with an invoice.
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, verbose_name='factura')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='servicio')

    class Meta:
        verbose_name = 'servicio de una factura'
        verbose_name_plural = 'servicios de facturas'

    def __str__(self):
        return "{0} - {1}".format(self.invoice, self.service)


class Transaction(models.Model):
    """
    Details a monetary transaction.
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, verbose_name='factura')
    payed_by = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='pagado por')
    datetime = models.DateTimeField(default=django.utils.timezone.now, verbose_name='fecha y hora')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='cantidad')

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
    authorized_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, verbose_name='autorizado por')

    class Meta:
        verbose_name = 'costo de una reparación'
        verbose_name_plural = 'costos de reparaciones'

    def __str__(self):
        return "{0}: ${1}".format(self.repair, self.cost)
