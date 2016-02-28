from back_office.models import Employee, Client, BranchOffice
from django.db import models


class UnitOfMeasurement:
    """Magnitude of a physical quantity."""
    METER = 0
    KILOGRAM = 1
    SECOND = 2
    PIECE = 3
    UNIT_CHOICES = (
        (METER, "m"),
        (KILOGRAM, "Kg"),
        (SECOND, "s"),
        (PIECE, "pz"),
    )


class ProductDefinition(models.Model):
    """
    The definition of a product manufactured by Acrilfrasa.
    """
    sku = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=100, blank=True)
    short_description = models.CharField(max_length=50, blank=True)
    image = models.ImageField()
    color = models.CharField(max_length=10)
    length = models.DecimalField(max_digits=6, decimal_places=2, default=0.01)
    width = models.DecimalField(max_digits=6, decimal_places=2, default=0.01)
    thickness = models.DecimalField(max_digits=6, decimal_places=2, default=0.01)
    weight = models.DecimalField(max_digits=6, decimal_places=2, default=0.01)
    is_composite = models.BooleanField(default=False)
    unit = models.PositiveSmallIntegerField(choices=UnitOfMeasurement.UNIT_CHOICES)


class WorkOrder(models.Model):
    """
    An order that authorizes the manufacture of a product.
    """
    number = models.CharField(max_length=50, primary_key=True)
    product_definition = models.ForeignKey(ProductDefinition, on_delete=models.CASCADE)
    authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT)
    authorization_datetime = models.DateTimeField()


class Product(models.Model):
    """
    A concrete product manufactured by Acrilfrasa.
    """
    IN_MANUFACTURING = 0
    IN_WAREHOUSE = 1
    SOLD = 2
    RETURNED = 3
    DESTROYED = 4
    STATE_CHOICES = (
        (IN_MANUFACTURING, "En producción"),
        (IN_WAREHOUSE, "En almacén"),
        (SOLD, "Vendido"),
        (RETURNED, "Devuelto"),
        (DESTROYED, "Destruido"),
    )

    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES)
    number = models.CharField(max_length=50, primary_key=True)
    definition = models.ForeignKey(ProductDefinition, on_delete=models.CASCADE)
    manufacture_date = models.DateField()
    manufacturer = models.ForeignKey(Employee, on_delete=models.PROTECT)
    manufacture_order = models.ForeignKey("WorkOrder", on_delete=models.PROTECT)


class MaterialDefinition(models.Model):
    """
    Definition of a miscelaneous material used for individual sale or for
    the production of composite products.
    """
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=50)
    image = models.ImageField()
    color = models.CharField(max_length=10)
    length = models.DecimalField(max_digits=6, decimal_places=2, default=0.01)
    width = models.DecimalField(max_digits=6, decimal_places=2, default=0.01)
    thickness = models.DecimalField(max_digits=6, decimal_places=2, default=0.01)
    weight = models.DecimalField(max_digits=6, decimal_places=2, default=0.01)
    unit = models.PositiveSmallIntegerField(choices=UnitOfMeasurement.UNIT_CHOICES)


class ProductComponent(models.Model):
    """
    Describes the quantity of a specific material
    needed for a composite product.
    """
    name = models.CharField(max_length=45)
    product = models.ForeignKey(ProductDefinition, on_delete=models.CASCADE)
    material = models.ForeignKey(MaterialDefinition, on_delete=models.CASCADE)
    unit = models.PositiveSmallIntegerField(choices=UnitOfMeasurement.UNIT_CHOICES)
    required_units = models.PositiveSmallIntegerField(default=1)
    required_amount_per_unit = models.DecimalField(default=1.00, max_digits=5, decimal_places=2)


class ProductInventoryItem(models.Model):
    """An entry of a specific product in an inventory."""
    product = models.ForeignKey(ProductDefinition, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)


class ProductsInventory(models.Model):
    """An inventory of various products."""
    name = models.CharField(max_length=45)
    supervisor = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="products_inventories_supervised")
    branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE)
    items = models.ManyToManyField(ProductInventoryItem)
    last_update = models.DateTimeField(auto_now=True)
    last_updater = models.ForeignKey(Employee, on_delete=models.PROTECT)


class Material(models.Model):
    """
    Miscelaneous material used for individual sale or for
    the production of composite products.
    """
    IN_WAREHOUSE = 0
    USED_IN_PRODUCT = 1
    RETURNED = 2
    DESTROYED = 3
    STATE_CHOICES = (
        (IN_WAREHOUSE, "En producción"),
        (USED_IN_PRODUCT, "En producto"),
        (RETURNED, "Devuelto"),
        (DESTROYED, "Destruido"),
    )

    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES)
    number = models.CharField(max_length=50, primary_key=True)
    definition = models.ForeignKey(MaterialDefinition, on_delete=models.CASCADE)
    acquisition_date = models.DateField()
    buyer = models.ForeignKey(Employee, on_delete=models.PROTECT)
    authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="materials_authorized")


class MaterialInventoryItem(models.Model):
    """An entry of a specific material in an inventory."""
    material = models.ForeignKey(MaterialDefinition, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)


class MaterialsInventory(models.Model):
    """An inventory of various material."""
    name = models.CharField(max_length=45)
    supervisor = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="materials_inventories_supervised")
    branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE)
    items = models.ManyToManyField(MaterialInventoryItem)
    last_update = models.DateTimeField(auto_now=True)
    last_updater = models.ForeignKey(Employee, on_delete=models.PROTECT)


class ConsumableDefinition(models.Model):
    """
    Definition for any good that may be destroyed, dissipated, wasted or spent.
    """
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=50)
    image = models.ImageField()
    brand = models.CharField(max_length=45)
    model = models.CharField(max_length=45)
    unit = models.PositiveSmallIntegerField(choices=UnitOfMeasurement.UNIT_CHOICES)


class Consumable(models.Model):
    """
    Good that may be destroyed, dissipated, wasted or spent.
    """
    number = models.CharField(max_length=50, primary_key=True)
    definition = models.ForeignKey(ConsumableDefinition, on_delete=models.CASCADE)
    acquisition_date = models.DateField()
    buyer = models.ForeignKey(Employee, on_delete=models.PROTECT)
    authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="consumables_authorized")


class ConsumableInventoryItem(models.Model):
    """
    An entry of a specific consumable in an inventory.
    """
    consumable = models.ForeignKey(ConsumableDefinition, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)


class ConsumablesInventory(models.Model):
    """
    An inventory of various consumables.
    """
    name = models.CharField(max_length=45)
    supervisor = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                   related_name="consumables_inventories_supervised")
    branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE)
    items = models.ManyToManyField(ConsumableInventoryItem)
    last_update = models.DateTimeField(auto_now=True)
    last_updater = models.ForeignKey(Employee, on_delete=models.PROTECT)


class DurableGoodDefinition(models.Model):
    """
    Definition of a good that doesn't quickly wear out and yields utility over time.
    """
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=50)
    image = models.ImageField()
    brand = models.CharField(max_length=45)
    model = models.CharField(max_length=45)
    unit = models.PositiveSmallIntegerField(choices=UnitOfMeasurement.UNIT_CHOICES)


class DurableGood(models.Model):
    """
    Good that doesn't quickly wear out and yields utility over time.
    """
    number = models.CharField(max_length=50, primary_key=True)
    definition = models.ForeignKey(DurableGoodDefinition, on_delete=models.CASCADE)
    acquisition_date = models.DateField()
    buyer = models.ForeignKey(Employee, on_delete=models.PROTECT)
    authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="durable_goods_authorized")


class DurableGoodInventoryItem(models.Model):
    """
    An entry of a specific durable good in an inventory.
    """
    durable_good = models.ForeignKey(DurableGoodDefinition, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)


class DurableGoodsInventory(models.Model):
    """
    An inventory of various durable goods.
    """
    name = models.CharField(max_length=45)
    supervisor = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                   related_name="durable_goods_inventories_supervised")
    branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE)
    items = models.ManyToManyField(DurableGoodInventoryItem)
    last_update = models.DateTimeField(auto_now=True)
    last_updater = models.ForeignKey(Employee, on_delete=models.PROTECT)


class Movement(models.Model):
    """
    The record of an asset's movement within the company.
    """
    CREATION = 0
    EDITION = 1
    DELETION = 2
    TRANSFER = 3
    TYPE_CHOICES = (
        (CREATION, "Creación"),
        (EDITION, "Edición"),
        (DELETION, "Eliminación"),
        (TRANSFER, "Transferencia"),
    )

    PRODUCT = 0
    MATERIAL = 1
    EMPLOYEE = 2
    DURABLE_GOOD = 3
    TARGET_CHOICES = (
        (PRODUCT, "Producto"),
        (MATERIAL, "Material"),
        (EMPLOYEE, "Empleado"),
        (EMPLOYEE, "Recurso"),
    )

    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    target = models.PositiveSmallIntegerField(choices=TARGET_CHOICES)
    datetime = models.DateTimeField(auto_now_add=True)
    made_by = models.ForeignKey(Employee, on_delete=models.PROTECT)
