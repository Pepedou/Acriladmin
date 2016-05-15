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


class Product(models.Model):
    """
    The definition of a product manufactured by Acrilfrasa.
    """
    ACRYLIC = 0
    POLYCARBONATE = 1
    CELLULAR = 2
    PLASTIC = 3
    SHEET = 4
    GRIDS = 5
    DOMES = 6
    SILICON = 7
    NOT_LISTED = 8
    LINE_TYPES = (
        (ACRYLIC, "Acrílico"),
        (POLYCARBONATE, "Policarbonato"),
        (CELLULAR, "Celular"),
        (PLASTIC, "Plástico"),
        (SHEET, "Lámina"),
        (GRIDS, "Rejillas"),
        (DOMES, "Domos"),
        (SILICON, "Silicones"),
        (NOT_LISTED, "Otra")
    )

    sku = models.CharField(max_length=45, primary_key=True, verbose_name='SKU')
    description = models.CharField(max_length=100, verbose_name='descripción')
    line = models.PositiveSmallIntegerField(verbose_name='línea', choices=LINE_TYPES, default=NOT_LISTED)
    engraving = models.CharField(max_length=45, verbose_name='grabado', blank=True)
    color = models.CharField(blank=True, max_length=10, verbose_name='color')
    length = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='longitud (m)')
    width = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='anchura (m)')
    thickness = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='espesor (mm)')
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

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='producto')
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


class ProductReimbursement(models.Model):
    """
    A product or material reimbursement.
    """
    monetary_difference = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='diferencia')
    date = models.DateField(default=django.utils.timezone.now, verbose_name='fecha de devolución')
    to_branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE,
                                  related_name='product_reimbursement_as_to_branch', verbose_name='a la sucursal')
    from_branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='product_reimbursement_as_from_branch', verbose_name='de la sucursal')

    class Meta:
        verbose_name = 'devolución de productos'
        verbose_name_plural = 'devoluciones de productos'

    def __str__(self):
        return self.id

    def clean(self):
        # TODO: Test this method
        super(ProductReimbursement, self).clean()

        if self.id is not None:
            return

        to_inventory = self.to_branch.productsinventory

        if to_inventory is None:
            raise ValidationError({
                'to_branch': 'La sucursal de origen no cuenta con un inventario de productos.'
            })

        if self.from_branch is not None:
            self._clean_exchange_target_branch()

        elif len(self.exchangedproduct_set) != 0:
            raise ValidationError({
                'from_inventory': 'No se pueden elegir productos a intercambiar sin haber seleccionado '
                                  'de qué sucursal se van a obtener.'
            })

    def _clean_exchange_target_branch(self):
        """
        Performs the necessary validations on the exchange's target branch.
        """
        from_inventory = self.from_branch.productsinventory

        if from_inventory is None:
            raise ValidationError({
                'from_inventory': 'La sucursal de destino no cuenta con un inventario de productos.'
            })

        exchanged_products_skus = [item.product.sku for item in self.exchangedproduct_set.all()]
        filtered_exchanged_products = from_inventory.productinventoryitem_set.filter(
            product__sku__in=exchanged_products_skus)

        if len(filtered_exchanged_products) < len(exchanged_products_skus):
            ProductReimbursement._raise_missing_products_error(filtered_exchanged_products)

        items_with_insufficient_stock = []

        for exchanged_product in self.exchangedproduct_set.all():
            for inventory_product in filtered_exchanged_products:
                if exchanged_product.product.sku == inventory_product.product.sku \
                        and exchanged_product.quantity > inventory_product.quantity:
                    items_with_insufficient_stock.append(exchanged_product)
                    break

        if len(items_with_insufficient_stock) > 0:
            self._raise_out_of_stock_error(items_with_insufficient_stock)

    def _raise_missing_products_error(self, filtered_exchanged_products):
        """
        Raises a ValidationError because some products are missing from the exchange's
        target branch.
        :param filtered_exchanged_products: The products available in the inventory.
        """
        missing_products = [item.product for item in self.exchangedproduct_set.all() if
                            item not in filtered_exchanged_products]
        missing_products_names = ""
        for item in missing_products:
            missing_products_names = "{0}, ".format(str(item))
        missing_products_names = missing_products_names[:len(missing_products_names) - 2]
        error_message = 'El inventario de la sucursal no cuenta con los siguientes productos: {0}'.format(
            missing_products_names)
        raise ValidationError({
            'from_branch': error_message
        })

    @staticmethod
    def _raise_out_of_stock_error(items_with_insufficient_stock):
        """
        Raises a ValidationError because some products are out of stock in the exchange's
        target branch.
        :param items_with_insufficient_stock: The missing items.
        """
        product_names = ""

        for item in items_with_insufficient_stock:
            product_names = "del {0} cuenta con {1}, ".format(str(item.product), str(item.quantity))

        product_names = product_names[:len(product_names) - 2]

        error_message = 'El inventario de la sucursal no cuenta con ' \
                        'la cantidad suficiente de los siguientes productos: {0}'.format(product_names)

        raise ValidationError({
            'from_branch': error_message
        })

    def save(self, *args, **kwargs):
        # TODO: Missing implementation
        pass

    def delete(self, using=None, keep_parents=False):
        # TODO: Missing implementation
        pass


class ReturnedProduct(models.Model):
    """
    Represents a tuple consisting of a Product and a quantity
    of that product that were returned.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='producto')
    quantity = models.PositiveIntegerField(default=1, verbose_name='cantidad')
    reimbursement = models.ForeignKey(ProductReimbursement, on_delete=models.CASCADE, verbose_name='devolución')

    class Meta:
        verbose_name = 'producto devuelto (entra)'
        verbose_name_plural = 'productos devueltos (entran)'

    def clean(self):
        if self.quantity == 0:
            raise ValidationError({
                'quantity': 'La cantidad debe ser mayor a 0.'
            })


class ExchangedProduct(models.Model):
    """
    Represents a tuple consisting of a Product and a quantity
    of that product that were asked in exchange for others.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='producto')
    quantity = models.PositiveIntegerField(default=1, verbose_name='cantidad')
    reimbursement = models.ForeignKey(ProductReimbursement, on_delete=models.CASCADE, verbose_name='devolución')

    class Meta:
        verbose_name = 'producto intercambiado (sale)'
        verbose_name_plural = 'productos intercambiados (salen)'

    def clean(self):
        if self.quantity == 0:
            raise ValidationError({
                'quantity': 'La cantidad debe ser mayor a 0.'
            })
