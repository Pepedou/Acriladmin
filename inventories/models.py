import django
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Q

from back_office.models import Employee, Client, BranchOffice, EmployeeRole


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


class Product(models.Model):
    """
    The definition of a product manufactured by Acrilfrasa.
    """
    ACR = 0
    ACRILETA = 1
    ACRIMP = 2
    ACRIP = 3
    ADE = 4
    DIFUSOR = 5
    DOM = 6
    GLASLINER = 7
    LAM = 8
    OTROS = 9
    PERFIL = 10
    PLA = 11
    POL = 12
    POL_SOL = 13
    SILI = 14
    STON = 15

    LINE_TYPES = (
        (ACR, "ACR"),
        (ACRILETA, "ACRILETA"),
        (ACRIMP, "ACRIMP"),
        (ACRIP, "ACRIP"),
        (ADE, "ADE"),
        (DIFUSOR, "DIFUSOR"),
        (DOM, "DOM"),
        (GLASLINER, "GLASLINER"),
        (LAM, "LAM"),
        (OTROS, "OTROS"),
        (PERFIL, "PERFIL"),
        (PLA, "PLA"),
        (POL, "POL"),
        (POL_SOL, "POL_SOL"),
        (SILI, "SILI"),
        (STON, "STON")

    )

    sku = models.CharField(max_length=45, unique=True, verbose_name='SKU')
    description = models.CharField(max_length=100, verbose_name='descripción')
    search_description = models.CharField(max_length=100, verbose_name='descripción para búsqueda')
    line = models.PositiveSmallIntegerField(verbose_name='línea', choices=LINE_TYPES, default=OTROS)
    engraving = models.CharField(max_length=45, verbose_name='grabado', blank=True)
    color = models.CharField(blank=True, max_length=20, verbose_name='color')
    length = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='longitud (m)')
    thickness = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='espesor (mm)')
    width = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='anchura (m)')
    is_composite = models.BooleanField(default=False, verbose_name='es compuesto')

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    def __str__(self):
        return self.description

    @staticmethod
    def get_products_without_price():
        """
        Returns all the products which do not yet have a price assigned to them.
        :return: Queryset with the products that match the condition.
        """
        return Product.objects.filter(productprice__isnull=True)


class Material(models.Model):
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='producto',
                                limit_choices_to=
                                {
                                    'is_composite': True
                                })
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='material')
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
                                   limit_choices_to=Q(roles__name=EmployeeRole.WAREHOUSE_CHIEF) & ~Q(username='root'))
    branch = models.OneToOneField(BranchOffice, on_delete=models.CASCADE, verbose_name='sucursal')
    last_update = models.DateTimeField(auto_now=True, verbose_name='última actualización')
    last_updater = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                     verbose_name='autor de la última actualización',
                                     limit_choices_to=~Q(username='root'))

    class Meta:
        verbose_name = 'inventario de productos'
        verbose_name_plural = 'inventarios de productos'

    def __str__(self):
        return self.name


class ProductInventoryItem(models.Model):
    """
    An entry of a specific product in an inventory.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='producto')
    quantity = models.PositiveIntegerField(default=0, verbose_name='cantidad')
    inventory = models.ForeignKey(ProductsInventory, on_delete=models.CASCADE, verbose_name='inventario')

    class Meta:
        verbose_name = 'elemento de inventario de productos'
        verbose_name_plural = 'elementos de inventario de productos'

    def __str__(self):
        return "{0}: {1}".format(self.product, self.quantity)


class MaterialsInventory(models.Model):
    """An inventory of various materials."""
    name = models.CharField(max_length=45, verbose_name='nombre')
    supervisor = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="materials_inventories_supervised",
                                   verbose_name='supervisor',
                                   limit_choices_to=Q(roles__name=EmployeeRole.ADMINISTRATOR) & ~Q(username='root'))
    branch = models.OneToOneField(BranchOffice, on_delete=models.CASCADE, verbose_name='sucursal')
    last_update = models.DateTimeField(auto_now=True, verbose_name='última actualización')
    last_updater = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                     verbose_name='autor de la última actualización',
                                     limit_choices_to=~Q(username='root'))

    class Meta:
        verbose_name = 'inventario de materiales'
        verbose_name_plural = 'inventarios de materiales'

    def __str__(self):
        return self.name


class MaterialInventoryItem(models.Model):
    """An entry of a specific material in an inventory."""
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='material')
    quantity = models.PositiveIntegerField(default=0, verbose_name='cantidad')
    inventory = models.ForeignKey(MaterialsInventory, on_delete=models.CASCADE, verbose_name='inventario')

    class Meta:
        verbose_name = 'elemento de inventario de materiales'
        verbose_name_plural = 'elementos de inventario de materiales'

    def __str__(self):
        return "{0}: {1}".format(self.material, self.quantity)


class Consumable(models.Model):
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


class ConsumablesInventory(models.Model):
    """
    An inventory of various consumables.
    """
    name = models.CharField(max_length=45, verbose_name='nombre')
    supervisor = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                   related_name="consumables_inventories_supervised", verbose_name='supervisor',
                                   limit_choices_to=Q(roles__name=EmployeeRole.ADMINISTRATOR) & ~Q(username='root'))
    branch = models.OneToOneField(BranchOffice, on_delete=models.CASCADE, verbose_name='sucursal')
    last_update = models.DateTimeField(auto_now=True, verbose_name='última actualización')
    last_updater = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                     verbose_name='autor de la última actualización',
                                     limit_choices_to=~Q(username='root'))

    class Meta:
        verbose_name = 'inventario de consumibles'
        verbose_name_plural = 'inventarios de consumibles'

    def __str__(self):
        return self.name


class ConsumableInventoryItem(models.Model):
    """
    An entry of a specific consumable in an inventory.
    """
    consumable = models.ForeignKey(Consumable, on_delete=models.CASCADE, verbose_name='consumible')
    quantity = models.PositiveIntegerField(default=0, verbose_name='cantidad')
    inventory = models.ForeignKey(ConsumablesInventory, on_delete=models.CASCADE, verbose_name='inventario')

    class Meta:
        verbose_name = 'elemento de inventario de consumibles'
        verbose_name_plural = 'elementos de inventario de consumibles'

    def __str__(self):
        return "{0}: {1}".format(self.consumable, self.quantity)


class DurableGood(models.Model):
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


class DurableGoodsInventory(models.Model):
    """
    An inventory of various durable goods.
    """
    name = models.CharField(max_length=45, verbose_name='nombre')
    supervisor = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                   related_name="durable_goods_inventories_supervised", verbose_name='supervisor',
                                   limit_choices_to=Q(roles__name=EmployeeRole.ADMINISTRATOR) & ~Q(username='root'))

    branch = models.OneToOneField(BranchOffice, on_delete=models.CASCADE, verbose_name='sucursal')
    last_update = models.DateTimeField(auto_now=True, verbose_name='última actualización')
    last_updater = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                     verbose_name='autor de la última actualización',
                                     limit_choices_to=~Q(username='root'))

    class Meta:
        verbose_name = 'inventario de activos'
        verbose_name_plural = 'inventarios de activos'

    def __str__(self):
        return self.name


class DurableGoodInventoryItem(models.Model):
    """
    An entry of a specific durable good in an inventory.
    """
    durable_good = models.ForeignKey(DurableGood, on_delete=models.CASCADE, verbose_name='activo')
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

    REJECTION_QUANTITY_MISMATCH = 0
    REJECTION_MATERIAL_MISMATCH = 1
    REJECTION_POOR_CONDITION = 2
    REJECTION_REASONS = (
        (REJECTION_QUANTITY_MISMATCH, "La cantidad recibida no concuerda con la esperada."),
        (REJECTION_MATERIAL_MISMATCH, "El material recibido no concuerda con el esperado."),
        (REJECTION_MATERIAL_MISMATCH, "El material se encuentra en mal estado.")
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='producto')
    source_branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE,
                                      related_name='product_transfers_as_source_branch',
                                      verbose_name='sucursal de origen')
    target_branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE,
                                      related_name='product_transfers_as_target_branch',
                                      verbose_name='sucursal de destino')
    quantity = models.PositiveIntegerField(verbose_name='cantidad')
    is_confirmed = models.BooleanField(default=False, verbose_name='confirmada')
    transfer_has_been_made = models.BooleanField(default=False, editable=False)
    rejection_reason = models.PositiveSmallIntegerField(null=True, blank=True, choices=REJECTION_REASONS,
                                                        verbose_name='motivo de rechazo')
    sale = models.ForeignKey('finances.Sale', on_delete=models.CASCADE, null=True, blank=True,
                             limit_choices_to=Q(state=1),
                             verbose_name='venta cancelada relacionada')

    class Meta:
        verbose_name = 'transferencia de productos'
        verbose_name_plural = 'transferencias de productos'

    def __str__(self):
        return "{0}: {1}".format(str(self.product), str(self.quantity))

    def clean(self):
        super(ProductTransfer, self).clean()

        if self.id is not None:
            if self.is_confirmed and self.rejection_reason is not None:
                raise ValidationError({
                    'rejection_reason': 'No se puede rechazar un producto cuya recepción está confirmada. '
                                        'Para hacerlo, deshabilite la confirmación o elimine el motivo de rechazo.'
                })
            elif not self.is_confirmed and self.rejection_reason is None:
                raise ValidationError({
                    'rejection_reason': 'Debe indicar un motivo para el rechazo de la transferencia.'
                })

            return

        try:
            source_inventory = self.source_branch.productsinventory
        except ProductsInventory.DoesNotExist:
            raise ValidationError({
                'source_branch': 'La sucursal de origen no cuenta con un inventario de productos. Hay que agregar '
                                 'uno antes de poder hacer una transferencia.'
            })

        try:
            self.target_branch.productsinventory
        except ProductsInventory.DoesNotExist:
            raise ValidationError({
                'target_branch': 'La sucursal de destino no cuenta con un inventario de productos.'
            })

        filtered_items = source_inventory.productinventoryitem_set.filter(product=self.product)

        if filtered_items.count() == 0:
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
        if self.is_confirmed and not self.transfer_has_been_made:
            source_inventory = self.source_branch.productsinventory
            target_inventory = self.target_branch.productsinventory

            source_inventory_item = source_inventory.productinventoryitem_set.filter(product=self.product).first()
            target_inventory_items = target_inventory.productinventoryitem_set.filter(product=self.product)

            source_inventory_item.quantity -= self.quantity

            if target_inventory_items.count() == 0:
                target_inventory_item = ProductInventoryItem()
                target_inventory_item.product = self.product
                target_inventory_item.inventory = target_inventory
            else:
                target_inventory_item = target_inventory_items.first()

            target_inventory_item.quantity += self.quantity

            self.transfer_has_been_made = True

            with transaction.atomic():
                target_inventory_item.save()
                source_inventory_item.save()
                super(ProductTransfer, self).save(*args, **kwargs)
        else:
            super(ProductTransfer, self).save(*args, **kwargs)


class ProductReimbursement(models.Model):
    """
    A product or material reimbursement.
    """

    @property
    def folio(self):
        """
        Returns a folio created base on the reimbursement's ID.
        :return: The folio as a string.
        """
        return "D{0}".format(str(self.id).zfill(9))

    date = models.DateField(default=django.utils.timezone.now, verbose_name='fecha de devolución')
    inventory = models.ForeignKey(ProductsInventory, on_delete=models.PROTECT, verbose_name='inventario')
    monetary_difference = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='diferencia')
    sale = models.ForeignKey('finances.Sale', on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='venta relacionada')

    class Meta:
        verbose_name = 'devolución de productos'
        verbose_name_plural = 'devoluciones de productos'

    def __str__(self):
        return self.folio


class ReturnedProduct(models.Model):
    """
    Represents a tuple consisting of a Product and a quantity
    that states how many units of that product were returned.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='producto')
    quantity = models.PositiveIntegerField(default=1, verbose_name='cantidad')
    reimbursement = models.ForeignKey(ProductReimbursement, on_delete=models.CASCADE, verbose_name='devolución')

    class Meta:
        verbose_name = 'producto devuelto (entra)'
        verbose_name_plural = 'productos devueltos (entran)'

    def __str__(self):
        return str(self.id)

    def clean(self):
        super(ReturnedProduct, self).clean()

        if self.quantity == 0:
            raise ValidationError({
                'quantity': 'La cantidad debe ser mayor a 0.'
            })

        from finances.models import ProductPrice
        product_price = ProductPrice.objects.filter(product=self.product).first()

        if product_price is None:
            raise ValidationError({
                'product': 'Este producto no cuenta con un precio. Solicite que se le asigne un precio '
                           'para poder completar la devolución.'
            })

    def save(self):
        if self.pk is not None:
            super(ReturnedProduct, self).save()
            return

        inventory = self.reimbursement.inventory

        inventory_product_items = inventory.productinventoryitem_set.filter(product=self.product)

        if inventory_product_items.count() == 0:
            inventory_item = ProductInventoryItem()
            inventory_item.product = self.product
            inventory_item.inventory = inventory
        else:
            inventory_item = inventory_product_items.first()

        inventory_item.quantity += self.quantity

        with transaction.atomic():
            inventory_item.save()
            super(ReturnedProduct, self).save()
