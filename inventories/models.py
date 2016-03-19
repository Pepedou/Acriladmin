from back_office.models import Employee, Client, BranchOffice
from django.db import models


class SIPrefix:
    """
    Prefixes for the International System of Units. The value
    stored is the power of ten to which the prefix corresponds.
    i.e. YOCTO = -24 because YOCTO = 10^-24.
    """
    NONE = 0
    YOCTO = -24
    ZEPTO = -21
    ATTO = -18
    FEMTO = -15
    PICO = -12
    NANO = -9
    MICRO = -6
    MILLI = -3
    CENTI = -2
    DECI = -1
    DECA = 1
    HECTO = 2
    KILO = 3
    MEGA = 6
    GIGA = 9
    TERA = 12
    PETA = 15
    EXA = 18
    ZETTA = 21
    YOTTA = 24
    PREFIX_CHOICES = (
        (NONE, "N/A"),
        (YOCTO, "y"),
        (ZEPTO, "z"),
        (ATTO, "a"),
        (FEMTO, "f"),
        (PICO, "p"),
        (NANO, "n"),
        (MICRO, "μ"),
        (MILLI, "m"),
        (CENTI, "c"),
        (DECI, "d"),
        (DECA, "da"),
        (HECTO, "h"),
        (KILO, "k"),
        (MEGA, "M"),
        (GIGA, "G"),
        (TERA, "T"),
        (PETA, "P"),
        (EXA, "E"),
        (ZETTA, "Z"),
        (YOTTA, "Y"),
    )


class UnitOfMeasurement:
    """
    Magnitude of a physical quantity.
    """
    NONE = 0
    METER = 1
    INCH = 2
    FOOT = 3
    YARD = 4
    MILE = 5
    GRAM = 6
    SECOND = 7
    PIECE = 8
    LITRE = 9
    UNIT_CHOICES = (
        (NONE, "N/A"),
        (METER, "m"),
        (INCH, "in"),
        (FOOT, "ft"),
        (YARD, "yd"),
        (MILE, "mi"),
        (GRAM, "g"),
        (SECOND, "s"),
        (PIECE, "pz"),
        (LITRE, "l"),
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
    prefix = models.SmallIntegerField(choices=SIPrefix.PREFIX_CHOICES, default=SIPrefix.NONE, blank=True)
    unit = models.PositiveSmallIntegerField(default=UnitOfMeasurement.NONE, choices=UnitOfMeasurement.UNIT_CHOICES)

    def __str__(self):
        return self.sku


class WorkOrder(models.Model):
    """
    An order that authorizes the manufacture of a product.
    """
    number = models.CharField(max_length=50, primary_key=True)
    product_definition = models.ForeignKey(ProductDefinition, on_delete=models.CASCADE)
    authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT)
    authorization_datetime = models.DateTimeField()

    def __str__(self):
        return str(self.number)


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

    def __str__(self):
        return str(self.state)


class MaterialDefinition(models.Model):
    """
    Definition of a miscelaneous material used for individual sale or for
    the production of composite products.
    """
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=50)
    image = models.FileField(blank=True)
    color = models.CharField(max_length=10)
    length = models.DecimalField(max_digits=6, decimal_places=2, default=0.01)
    width = models.DecimalField(max_digits=6, decimal_places=2, default=0.01)
    thickness = models.DecimalField(max_digits=6, decimal_places=2, default=0.01)
    weight = models.DecimalField(max_digits=6, decimal_places=2, default=0.01)
    prefix = models.SmallIntegerField(choices=SIPrefix.PREFIX_CHOICES, default=SIPrefix.NONE, blank=True)
    unit = models.PositiveSmallIntegerField(default=UnitOfMeasurement.NONE, choices=UnitOfMeasurement.UNIT_CHOICES)

    def __str__(self):
        return self.name


class ProductComponent(models.Model):
    """
    Describes the quantity of a specific material
    needed for a composite product.
    """
    name = models.CharField(max_length=45)
    product = models.ForeignKey(ProductDefinition, on_delete=models.CASCADE)
    material = models.ForeignKey(MaterialDefinition, on_delete=models.CASCADE)
    prefix = models.SmallIntegerField(choices=SIPrefix.PREFIX_CHOICES, default=SIPrefix.NONE, blank=True)
    unit = models.PositiveSmallIntegerField(default=UnitOfMeasurement.NONE, choices=UnitOfMeasurement.UNIT_CHOICES)
    required_units = models.PositiveSmallIntegerField(default=1)
    required_amount_per_unit = models.DecimalField(default=1.00, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class ProductInventoryItem(models.Model):
    """An entry of a specific product in an inventory."""
    product = models.ForeignKey(ProductDefinition, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{0}: {1}".format(self.product, self.quantity)


class ProductsInventory(models.Model):
    """An inventory of various products."""
    name = models.CharField(max_length=45)
    supervisor = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="products_inventories_supervised")
    branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE)
    items = models.ManyToManyField(ProductInventoryItem, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    last_updater = models.ForeignKey(Employee, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


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
        (IN_WAREHOUSE, "En almacén"),
        (USED_IN_PRODUCT, "Parte de un producto"),
        (RETURNED, "Devuelto"),
        (DESTROYED, "Destruido"),
    )

    number = models.CharField(max_length=50, primary_key=True)
    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES)
    definition = models.ForeignKey(MaterialDefinition, on_delete=models.CASCADE)
    acquisition_date = models.DateField()
    buyer = models.ForeignKey(Employee, on_delete=models.PROTECT)
    authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="materials_authorized")

    def __str__(self):
        return self.number


class MaterialInventoryItem(models.Model):
    """An entry of a specific material in an inventory."""
    material = models.ForeignKey(MaterialDefinition, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{0}: {1}".format(self.material, self.quantity)


class MaterialsInventory(models.Model):
    """An inventory of various material."""
    name = models.CharField(max_length=45)
    supervisor = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="materials_inventories_supervised")
    branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE)
    items = models.ManyToManyField(MaterialInventoryItem, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    last_updater = models.ForeignKey(Employee, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class ConsumableDefinition(models.Model):
    """
    Definition for any good that may be destroyed, dissipated, wasted or spent.
    """
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=50)
    image = models.ImageField()
    brand = models.CharField(max_length=45)
    model = models.CharField(max_length=45)
    prefix = models.SmallIntegerField(choices=SIPrefix.PREFIX_CHOICES, default=SIPrefix.NONE, blank=True)
    unit = models.PositiveSmallIntegerField(default=UnitOfMeasurement.NONE, choices=UnitOfMeasurement.UNIT_CHOICES)

    def __str__(self):
        return self.name


class Consumable(models.Model):
    """
    Good that may be destroyed, dissipated, wasted or spent.
    """
    number = models.CharField(max_length=50, primary_key=True)
    definition = models.ForeignKey(ConsumableDefinition, on_delete=models.CASCADE)
    acquisition_date = models.DateField()
    buyer = models.ForeignKey(Employee, on_delete=models.PROTECT)
    authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="consumables_authorized")

    def __str__(self):
        return self.number


class ConsumableInventoryItem(models.Model):
    """
    An entry of a specific consumable in an inventory.
    """
    consumable = models.ForeignKey(ConsumableDefinition, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{0}: {1}".format(self.consumable, self.quantity)


class ConsumablesInventory(models.Model):
    """
    An inventory of various consumables.
    """
    name = models.CharField(max_length=45)
    supervisor = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                   related_name="consumables_inventories_supervised")
    branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE)
    items = models.ManyToManyField(ConsumableInventoryItem, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    last_updater = models.ForeignKey(Employee, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class DurableGoodDefinition(models.Model):
    """
    Definition of a good that doesn't quickly wear out and yields utility over time.
    """
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=50)
    image = models.ImageField()
    brand = models.CharField(max_length=45)
    model = models.CharField(max_length=45)
    prefix = models.SmallIntegerField(default=SIPrefix.NONE, choices=SIPrefix.PREFIX_CHOICES)
    unit = models.PositiveSmallIntegerField(default=UnitOfMeasurement.NONE, choices=UnitOfMeasurement.UNIT_CHOICES)

    def __str__(self):
        return self.name


class DurableGood(models.Model):
    """
    Good that doesn't quickly wear out and yields utility over time.
    """
    number = models.CharField(max_length=50, primary_key=True)
    definition = models.ForeignKey(DurableGoodDefinition, on_delete=models.CASCADE)
    acquisition_date = models.DateField()
    buyer = models.ForeignKey(Employee, on_delete=models.PROTECT)
    authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="durable_goods_authorized")

    def __str__(self):
        return self.number


class DurableGoodInventoryItem(models.Model):
    """
    An entry of a specific durable good in an inventory.
    """
    durable_good = models.ForeignKey(DurableGoodDefinition, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{0}: {1}".format(self.durable_good, self.quantity)


class DurableGoodsInventory(models.Model):
    """
    An inventory of various durable goods.
    """
    name = models.CharField(max_length=45)
    supervisor = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                   related_name="durable_goods_inventories_supervised")
    branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE)
    items = models.ManyToManyField(DurableGoodInventoryItem, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    last_updater = models.ForeignKey(Employee, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


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
    CONSUMABLE = 3
    DURABLE_GOOD = 4
    TARGET_CHOICES = (
        (PRODUCT, "Producto"),
        (MATERIAL, "Material"),
        (EMPLOYEE, "Empleado"),
        (CONSUMABLE, "Consumible"),
        (DURABLE_GOOD, "Recurso"),
    )

    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    target = models.PositiveSmallIntegerField(choices=TARGET_CHOICES)
    datetime = models.DateTimeField(auto_now_add=True)
    made_by = models.ForeignKey(Employee, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, null=True, blank=True)
    consumable = models.ForeignKey(Consumable, on_delete=models.CASCADE, null=True, blank=True)
    durable_good = models.ForeignKey(DurableGood, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "{0}: {1}".format(self.type, self.target)
