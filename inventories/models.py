import django
from back_office.models import Employee, Client, BranchOffice, EmployeeRole
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, transaction


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
    sku = models.CharField(max_length=45, primary_key=True, verbose_name='SKU')
    name = models.CharField(max_length=45, verbose_name='nombre')
    short_description = models.CharField(max_length=50, blank=True, verbose_name='descripción corta')
    description = models.TextField(blank=True, verbose_name='descripción')
    image = models.ImageField(blank=True, verbose_name='imagen')
    color = models.CharField(blank=True, max_length=10, verbose_name='color')
    length = models.DecimalField(max_digits=6, decimal_places=2, default=0.01, verbose_name='longitud')
    width = models.DecimalField(max_digits=6, decimal_places=2, default=0.01, verbose_name='anchura')
    thickness = models.DecimalField(max_digits=6, decimal_places=2, default=0.01, verbose_name='grosor')
    weight = models.DecimalField(max_digits=6, decimal_places=2, default=0.01, verbose_name='peso')
    prefix = models.SmallIntegerField(choices=SIPrefix.PREFIX_CHOICES, default=SIPrefix.NONE, blank=True,
                                      verbose_name='prefijo de unidad')
    unit = models.PositiveSmallIntegerField(default=UnitOfMeasurement.NONE, choices=UnitOfMeasurement.UNIT_CHOICES,
                                            verbose_name='unidad')
    is_composite = models.BooleanField(default=False, verbose_name='es compuesto')

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    def __str__(self):
        return self.name

    @staticmethod
    def get_products_without_price():
        """
        Returns all the products which do not yet have a price assigned to them.
        :return: Queryset with the products that match the condition.
        """
        return ProductDefinition.objects.filter(productprice__isnull=True)


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

    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES, verbose_name='estado')
    definition = models.ForeignKey(ProductDefinition, on_delete=models.CASCADE, verbose_name='definición')
    manufacture_date = models.DateField(null=True, blank=True, verbose_name='fecha de manufactura')
    manufacturer = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True, blank=True,
                                     verbose_name='manufacturado por')

    class Meta:
        verbose_name = 'producto concreto'
        verbose_name_plural = 'productos concretos'

    def __str__(self):
        return str(self.state)


class MaterialDefinition(models.Model):
    """
    Definition of a miscelaneous material used for individual sale or for
    the production of composite products.
    """
    name = models.CharField(max_length=45, verbose_name='nombre')
    description = models.CharField(max_length=50, verbose_name='descripción')
    image = models.FileField(blank=True, verbose_name='imagen')
    color = models.CharField(max_length=10, default='color')
    length = models.DecimalField(max_digits=6, decimal_places=2, default=0.01, verbose_name='longitud')
    width = models.DecimalField(max_digits=6, decimal_places=2, default=0.01, verbose_name='anchura')
    thickness = models.DecimalField(max_digits=6, decimal_places=2, default=0.01, verbose_name='grosor')
    weight = models.DecimalField(max_digits=6, decimal_places=2, default=0.01, verbose_name='peso')
    prefix = models.SmallIntegerField(choices=SIPrefix.PREFIX_CHOICES, default=SIPrefix.NONE, blank=True,
                                      verbose_name='prefijo de unidad')
    unit = models.PositiveSmallIntegerField(default=UnitOfMeasurement.NONE, choices=UnitOfMeasurement.UNIT_CHOICES,
                                            verbose_name='unidad')

    class Meta:
        verbose_name = 'material'
        verbose_name_plural = 'materiales'

    def __str__(self):
        return self.name


class ProductComponent(models.Model):
    """
    Describes the quantity of a specific material
    needed for a composite product.
    """
    name = models.CharField(max_length=45, verbose_name='nombre')
    product = models.ForeignKey(ProductDefinition, on_delete=models.CASCADE, verbose_name='producto',
                                limit_choices_to=
                                {
                                    'is_composite': True
                                })
    material = models.ForeignKey(MaterialDefinition, on_delete=models.CASCADE, verbose_name='material')
    required_units = models.PositiveSmallIntegerField(default=1, verbose_name='unidades requeridas del componente')
    required_amount_per_unit = models.DecimalField(default=1.00, max_digits=5, decimal_places=2,
                                                   verbose_name='cantidad requerida por unidad')

    class Meta:
        verbose_name = 'componente de un producto'
        verbose_name_plural = 'componentes de productos'

    def __str__(self):
        return self.name


class ProductsInventory(models.Model):
    """An inventory of various products."""
    name = models.CharField(max_length=45, verbose_name='nombre')
    supervisor = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="products_inventories_supervised",
                                   verbose_name='supervisor',
                                   limit_choices_to=
                                   {
                                       'roles__name': EmployeeRole.WAREHOUSE_CHIEF
                                   })
    branch = models.OneToOneField(BranchOffice, on_delete=models.CASCADE, verbose_name='sucursal')
    last_update = models.DateTimeField(auto_now=True, verbose_name='última actualización')
    last_updater = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                     verbose_name='autor de la última actualización')

    class Meta:
        verbose_name = 'inventario de productos'
        verbose_name_plural = 'inventarios de productos'

    def __str__(self):
        return self.name


class ProductInventoryItem(models.Model):
    """
    An entry of a specific product in an inventory.
    """
    product = models.ForeignKey(ProductDefinition, on_delete=models.CASCADE, verbose_name='producto')
    quantity = models.PositiveIntegerField(default=0, verbose_name='cantidad')
    inventory = models.ForeignKey(ProductsInventory, on_delete=models.CASCADE, verbose_name='inventario')

    class Meta:
        verbose_name = 'elemento de inventario de productos'
        verbose_name_plural = 'elementos de inventario de productos'

    def __str__(self):
        return "{0}: {1}".format(self.product, self.quantity)


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

    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES, verbose_name='estado')
    definition = models.ForeignKey(MaterialDefinition, on_delete=models.CASCADE, verbose_name='definición')
    acquisition_date = models.DateField(default=django.utils.timezone.now, verbose_name='fecha de adquisición')
    buyer = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='comprador')
    authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="materials_authorized",
                                      blank=True,
                                      verbose_name='autorizado por')

    class Meta:
        verbose_name = 'material concreto'
        verbose_name_plural = 'materiales concretos'

    def __str__(self):
        return str(self.number)


class MaterialsInventory(models.Model):
    """An inventory of various materials."""
    name = models.CharField(max_length=45, verbose_name='nombre')
    supervisor = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="materials_inventories_supervised",
                                   verbose_name='supervisor',
                                   limit_choices_to=
                                   {
                                       'roles__name': EmployeeRole.ADMINISTRATOR
                                   })
    branch = models.OneToOneField(BranchOffice, on_delete=models.CASCADE, verbose_name='sucursal')
    last_update = models.DateTimeField(auto_now=True, verbose_name='última actualización')
    last_updater = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                     verbose_name='autor de la última actualización')

    class Meta:
        verbose_name = 'inventario de materiales'
        verbose_name_plural = 'inventarios de materiales'

    def __str__(self):
        return self.name


class MaterialInventoryItem(models.Model):
    """An entry of a specific material in an inventory."""
    material = models.ForeignKey(MaterialDefinition, on_delete=models.CASCADE, verbose_name='material')
    quantity = models.PositiveIntegerField(default=0, verbose_name='cantidad')
    inventory = models.ForeignKey(MaterialsInventory, on_delete=models.CASCADE, verbose_name='inventario')

    class Meta:
        verbose_name = 'elemento de inventario de materiales'
        verbose_name_plural = 'elementos de inventario de materiales'

    def __str__(self):
        return "{0}: {1}".format(self.material, self.quantity)


class ConsumableDefinition(models.Model):
    """
    Definition for any good that may be destroyed, dissipated, wasted or spent.
    """
    name = models.CharField(max_length=45, verbose_name='nombre')
    description = models.CharField(max_length=50, blank=True, verbose_name='descripción')
    image = models.ImageField(blank=True, verbose_name='imagen')
    brand = models.CharField(max_length=45, verbose_name='marca')
    model = models.CharField(max_length=45, verbose_name='modelo')
    prefix = models.SmallIntegerField(choices=SIPrefix.PREFIX_CHOICES, default=SIPrefix.NONE,
                                      verbose_name='prefijo de unidad')
    unit = models.PositiveSmallIntegerField(default=UnitOfMeasurement.NONE, choices=UnitOfMeasurement.UNIT_CHOICES,
                                            verbose_name='unidad')

    class Meta:
        verbose_name = 'consumible'
        verbose_name_plural = 'consumibles'

    def __str__(self):
        return self.name


class Consumable(models.Model):
    """
    Good that may be destroyed, dissipated, wasted or spent.
    """
    definition = models.ForeignKey(ConsumableDefinition, on_delete=models.CASCADE, verbose_name='definición')
    acquisition_date = models.DateField(verbose_name='fecha de adquisición')
    buyer = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='comprador')
    authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="consumables_authorized",
                                      blank=True,
                                      verbose_name='autorizado por')

    class Meta:
        verbose_name = 'consumible concreto'
        verbose_name_plural = 'consumibles concretos'

    def __str__(self):
        return self.number


class ConsumablesInventory(models.Model):
    """
    An inventory of various consumables.
    """
    name = models.CharField(max_length=45, verbose_name='nombre')
    supervisor = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                   related_name="consumables_inventories_supervised", verbose_name='supervisor',
                                   limit_choices_to=
                                   {
                                       'roles__name': EmployeeRole.ADMINISTRATOR
                                   })
    branch = models.OneToOneField(BranchOffice, on_delete=models.CASCADE, verbose_name='sucursal')
    last_update = models.DateTimeField(auto_now=True, verbose_name='última actualización')
    last_updater = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                     verbose_name='autor de la última actualización')

    class Meta:
        verbose_name = 'inventario de consumibles'
        verbose_name_plural = 'inventarios de consumibles'

    def __str__(self):
        return self.name


class ConsumableInventoryItem(models.Model):
    """
    An entry of a specific consumable in an inventory.
    """
    consumable = models.ForeignKey(ConsumableDefinition, on_delete=models.CASCADE, verbose_name='consumible')
    quantity = models.PositiveIntegerField(default=0, verbose_name='cantidad')
    inventory = models.ForeignKey(ConsumablesInventory, on_delete=models.CASCADE, verbose_name='inventario')

    class Meta:
        verbose_name = 'elemento de inventario de consumibles'
        verbose_name_plural = 'elementos de inventario de consumibles'

    def __str__(self):
        return "{0}: {1}".format(self.consumable, self.quantity)


class DurableGoodDefinition(models.Model):
    """
    Definition of a good that doesn't quickly wear out and yields utility over time.
    """
    name = models.CharField(max_length=45, verbose_name='nombre')
    description = models.CharField(max_length=50, verbose_name='descripción')
    image = models.ImageField(blank=True, verbose_name='imagen')
    brand = models.CharField(max_length=45, verbose_name='marca')
    model = models.CharField(max_length=45, verbose_name='modelo')
    prefix = models.SmallIntegerField(default=SIPrefix.NONE, choices=SIPrefix.PREFIX_CHOICES,
                                      verbose_name='prefijo de la unidad')
    unit = models.PositiveSmallIntegerField(default=UnitOfMeasurement.NONE, choices=UnitOfMeasurement.UNIT_CHOICES,
                                            verbose_name='unidad')

    class Meta:
        verbose_name = 'activo'
        verbose_name_plural = 'activos'

    def __str__(self):
        return self.name


class DurableGood(models.Model):
    """
    Good that doesn't quickly wear out and yields utility over time.
    """
    definition = models.ForeignKey(DurableGoodDefinition, on_delete=models.CASCADE, verbose_name='definición')
    acquisition_date = models.DateField(verbose_name='fecha de adquisición')
    buyer = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='comprador')
    authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="durable_goods_authorized",
                                      verbose_name='autorizado por',
                                      limit_choices_to=
                                      {
                                          'roles__name': EmployeeRole.ADMINISTRATOR
                                      })

    class Meta:
        verbose_name = 'activo concreto'
        verbose_name_plural = 'activos concretos'

    def __str__(self):
        return self.number


class DurableGoodsInventory(models.Model):
    """
    An inventory of various durable goods.
    """
    name = models.CharField(max_length=45, verbose_name='nombre')
    supervisor = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                   related_name="durable_goods_inventories_supervised", verbose_name='supervisor',
                                   limit_choices_to=
                                   {
                                       'roles__name': EmployeeRole.ADMINISTRATOR
                                   })
    branch = models.OneToOneField(BranchOffice, on_delete=models.CASCADE, verbose_name='sucursal')
    last_update = models.DateTimeField(auto_now=True, verbose_name='última actualización')
    last_updater = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                     verbose_name='autor de la última actualización')

    class Meta:
        verbose_name = 'inventario de activos'
        verbose_name_plural = 'inventarios de activos'

    def __str__(self):
        return self.name


class DurableGoodInventoryItem(models.Model):
    """
    An entry of a specific durable good in an inventory.
    """
    durable_good = models.ForeignKey(DurableGoodDefinition, on_delete=models.CASCADE, verbose_name='activo')
    quantity = models.PositiveIntegerField(default=0, verbose_name='cantidad')
    inventory = models.ForeignKey(DurableGoodsInventory, on_delete=models.CASCADE, verbose_name='inventario')

    class Meta:
        verbose_name = 'elemento de inventario de activos'
        verbose_name_plural = 'elementos de inventarios de activos'

    def __str__(self):
        return "{0}: {1}".format(self.durable_good, self.quantity)


class ProductTransfer(models.Model):
    """
    A transfer between two branches of a product.
    """

    product = models.ForeignKey(ProductDefinition, on_delete=models.CASCADE, verbose_name='producto')
    source_branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE,
                                      related_name='product_transfers_as_source_branch',
                                      verbose_name='sucursal de origen')
    target_branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE,
                                      related_name='product_transfers_as_target_branch',
                                      verbose_name='sucursal de destino')
    quantity = models.PositiveIntegerField(verbose_name='cantidad')
    is_confirmed = models.BooleanField(default=False, verbose_name='confirmada')

    class Meta:
        verbose_name = 'transferencia de producto'
        verbose_name_plural = 'transferencias de producto'

    def __str__(self):
        return "{0}: {1}".format(str(self.product), str(self.quantity))

    def clean(self):
        super(ProductTransfer, self).clean()

        if self.id is not None:
            return

        source_inventory = self.source_branch.productsinventory
        target_inventory = self.target_branch.productsinventory

        if source_inventory is None:
            raise ValidationError({
                'source_branch': 'La sucursal de origen no cuenta con un inventario de productos.'
            })

        if target_inventory is None:
            raise ValidationError({
                'target_branch': 'La sucursal de destino no cuenta con un inventario de productos.'
            })

        filtered_items = source_inventory.productinventoryitem_set.filter(product__sku=self.product.sku)

        if len(filtered_items) == 0:
            raise ValidationError({
                'product': 'El inventario de la sucursal de origen no cuenta con ese producto.'
            })

        inventory_item = filtered_items[0]

        if inventory_item.quantity < self.quantity:
            raise ValidationError({
                'quantity': 'El inventario de la sucursal de origen cuenta con {0} unidades de {1}.'.format(
                    inventory_item.quantity,
                    str(inventory_item.product))
            })

    def save(self, *args, **kwargs):
        if self.id is not None:
            super(ProductTransfer, self).save(*args, **kwargs)
            return

        source_inventory = self.source_branch.productsinventory
        target_inventory = self.target_branch.productsinventory

        source_inventory_item = source_inventory.productinventoryitem_set.filter(product__sku=self.product.sku)[0]
        target_inventory_items = target_inventory.productinventoryitem_set.filter(product__sku=self.product.sku)

        source_inventory_item.quantity -= self.quantity

        if len(target_inventory_items) == 0:
            target_inventory_item = ProductInventoryItem()
            target_inventory_item.product = self.product
            target_inventory_item.inventory = target_inventory
        else:
            target_inventory_item = target_inventory_items[0]

        target_inventory_item.quantity += self.quantity

        with transaction.atomic():
            target_inventory_item.save()
            source_inventory_item.save()

        super(ProductTransfer, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        source_inventory = self.source_branch.productsinventory[0]
        target_inventory = self.target_branch.productsinventory[0]

        source_inventory_items = source_inventory.productinventoryitem_set.filter(product__sku=self.product.sku)
        target_inventory_item = target_inventory.productinventoryitem_set.filter(product__sku=self.product.sku)[0]

        if len(source_inventory_items) == 0:
            source_inventory_item = ProductInventoryItem()
            source_inventory_item.product = self.product
            source_inventory_item.inventory = source_inventory
        else:
            source_inventory_item = source_inventory_items[0]

        source_inventory_item.quantity += self.quantity

        target_inventory_item.quantity -= self.quantity

        with transaction.atomic():
            target_inventory_item.save()
            source_inventory_item.save()

        super(ProductTransfer, self).delete(using, keep_parents)
