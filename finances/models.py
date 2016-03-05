import django

from back_office.models import Client, Employee
from django.db import models
from inventories.models import Product, Material
from operations.models import Service, Repair


class Order(models.Model):
    """
    An order of products made by a client.
    """
    PLACED = 0
    IN_PROGRESS = 1
    COMPLETE = 2
    CANCELLED = 3
    RETURNED = 4
    STATUS_CHOICES = (
        (PLACED, "Solicitada"),
        (IN_PROGRESS, "En progreso"),
        (COMPLETE, "Completa"),
        (CANCELLED, "Cancelada"),
        (RETURNED, "Devuelta"),
    )

    PRODUCTS = 0
    SERVICES = 1
    PRODUCTS_AND_SERVICES = 2
    TARGET_CHOICES = (
        (PRODUCTS, "Productos"),
        (SERVICES, "Servicios"),
        (PRODUCTS_AND_SERVICES, "Productos y servicios"),
    )

    @property
    def total(self):
        return self.subtotal + self.shipping_and_handling - self.discount

    number = models.CharField(verbose_name='número', max_length=50, primary_key=True)
    status = models.PositiveSmallIntegerField(verbose_name='estado', choices=STATUS_CHOICES)
    target = models.PositiveSmallIntegerField(verbose_name='objeto', choices=TARGET_CHOICES)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='cliente')
    date = models.DateField(verbose_name='fecha', default=django.utils.timezone.now)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_and_handling = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.number


class OrderProducts(models.Model):
    """
    An entry that relates a concrete product with an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __str__(self):
        return "{0} - {1}".format(self.order, self.product)


class OrderServices(models.Model):
    """
    An entry that relates a service with an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1}".format(self.order, self.service)


class Invoice(models.Model):
    """
    Commercial document issued by Acrilfrasa to a buyer related to a sale transaction
    and indicating the products, quantities and agreed prices for products or services
    provided.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    file = models.FileField(blank=True)

    def __str__(self):
        return str(self.order)


class ProductInvoice(models.Model):
    """
    An entry that relates a concrete product with an invoice.
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __str__(self):
        return "{0} - {1}".format(self.invoice, self.product)


class ProductPrice(models.Model):
    """
    Determines the price of a product.
    """
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT)

    def __str__(self):
        return self.price


class MaterialCost(models.Model):
    """
    Specifies the monetary cost of a material.
    """
    material = models.OneToOneField(Material, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT)

    def __str__(self):
        return self.cost


class ServiceInvoice(models.Model):
    """
    An entry that relates a service with an invoice.
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1}".format(self.invoice, self.service)


class Transaction(models.Model):
    """
    Details a monetary transaction.
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)
    payed_by = models.ForeignKey(Client, on_delete=models.PROTECT)
    datetime = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.amount


class RepairCost(models.Model):
    """
    The associated cost for a specific repair.
    """
    repair = models.ForeignKey(Repair, on_delete=models.PROTECT)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
