from back_office.models import Client
from django.db import models
from inventories.models import Product


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

    number = models.CharField(max_length=50, primary_key=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    target = models.PositiveSmallIntegerField(choices=TARGET_CHOICES)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    date = models.DateField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_and_handling = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)


class OrderProducts(models.Model):
    """
    An entry that relates a concrete product with an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)


class OrderServices(models.Model):
    """
    An entry that relates a service with an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # TODO: Add service model.


class Invoice(models.Model):
    """
    Commercial document issued by Acrilfrasa to a buyer relating to a sale transaction
    and indicating the products, quantities and agreed prices for products or services
    provided.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class InvoiceProducts(models.Model):
    """
    An entry that relates a concrete product with an invoice.
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)


class InvoiceServices(models.Model):
    """
    An entry that relates a service with an invoice.
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    # TODO: Add service model.
