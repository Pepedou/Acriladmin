import datetime
import sys

import django
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.db.models import Q

from back_office.models import Employee, Client, BranchOffice, EmployeeGroup, Provider


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
    width = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='anchura (m)')
    thickness = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='espesor (mm)')
    is_composite = models.BooleanField(default=False, verbose_name='es compuesto')
    is_scrap = models.BooleanField(default=False, editable=False, verbose_name='es pedacería')

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

    def get_absolute_url(self):
        """
        Returns the admin's change URL for this model.
        :return: The URL.
        """
        return reverse('admin:inventories_product_change', args=[str(self.id)])


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
                                   limit_choices_to=Q(groups__name=EmployeeGroup.WAREHOUSE_CHIEF) & ~Q(username='root'))
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
                                   limit_choices_to=Q(groups__name=EmployeeGroup.ADMINISTRATOR) & ~Q(username='root'))
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
                                   limit_choices_to=Q(groups__name=EmployeeGroup.ADMINISTRATOR) & ~Q(username='root'))
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
                                   limit_choices_to=Q(groups__name=EmployeeGroup.ADMINISTRATOR) & ~Q(username='root'))

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


class ProductTransferShipment(models.Model):
    """
    A shipment for the product's transfer between branches.
    """

    STATUS_CONFIRMED = 0
    STATUS_CANCELLED = 1
    STATUS_PENDING = 2
    STATUS_TYPES = (
        (STATUS_CONFIRMED, "Confirmado"),
        (STATUS_CANCELLED, "Cancelado"),
        (STATUS_PENDING, "Pendiente"),
    )

    source_branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE,
                                      editable=False,
                                      related_name='product_transfers_as_source_branch',
                                      verbose_name='sucursal de origen')
    target_branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE,
                                      related_name='product_transfers_as_target_branch',
                                      verbose_name='sucursal de destino')
    shipped_by_user = models.ForeignKey(Employee, on_delete=models.PROTECT, editable=False,
                                        related_name='shipped_product_transfers',
                                        verbose_name='enviado por')
    confirmed_by_user = models.ForeignKey(Employee, on_delete=models.PROTECT, editable=False, null=True,
                                          related_name='confirmed_product_transfers',
                                          verbose_name='confirmado por')
    date_shipped = models.DateTimeField(verbose_name='fecha de envío')
    date_confirmed = models.DateTimeField(null=True, blank=True, editable=False, verbose_name='fecha de confirmación')
    status = models.PositiveSmallIntegerField(choices=STATUS_TYPES, default=STATUS_PENDING,
                                              verbose_name='estado')

    class Meta:
        verbose_name = 'envío de transferencia de productos'
        verbose_name_plural = 'envíos de transferencia de productos'

    def __str__(self):
        return "Transferencia a {0}".format(str(self.target_branch))

    def confirm(self):
        """
        Confirms this product shipment. It sets its status to CONFIRMED
        and removes the products from the inventory.
        """
        with transaction.atomic():
            self.status = ProductTransferShipment.STATUS_CONFIRMED
            self.date_confirmed = datetime.datetime.now()
            self.save()

            for transferred_product in self.transferredproduct_set.all():
                inventory_item = self.source_branch.productsinventory.productinventoryitem_set.filter(
                    product=transferred_product.product).first()

                if not inventory_item:
                    raise ValueError('{0} no existe en el inventario {1}.'.format(str(
                        transferred_product.product),
                        str(self.source_branch.productsinventory)))

                inventory_item.quantity -= transferred_product.quantity
                inventory_item.save()

    def get_confirm_params_for_ajax_request(self):
        """
        Returns a dictionary with the parameters necessary for the 'confirmOrCancelInventoryMovement'
        AJAX call.
        :return: A dictionary with the parameters.
        """
        url = reverse('productmovconfirmorcancel')
        model = self.__class__.__name__
        pk = self.pk
        action = 'confirm'

        return {'url': url, 'model': model, 'pk': pk, 'action': action}

    def cancel(self):
        """
        Cancels this product transfer shipment. Sets its status to CANCELLED
        and no products are removed from the inventory.
        """
        self.status = ProductRemoval.STATUS_CANCELLED
        self.date_confirmed = datetime.datetime.now()
        self.save()

    def get_cancel_params_for_ajax_request(self):
        """
        Returns a dictionary with the parameters necessary for the 'confirmOrCancelInventoryMovement'
        AJAX call.
        :return: A dictionary with the parameters.
        """
        url = reverse('productmovconfirmorcancel')
        model = self.__class__.__name__
        pk = self.pk
        action = 'cancel'

        return {'url': url, 'model': model, 'pk': pk, 'action': action}


class TransferredProduct(models.Model):
    """
    The quantity of a product shipped in a product
    transfer shipment.
    """
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='producto')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='cantidad')
    product_transfer_shipment = models.ForeignKey(ProductTransferShipment, on_delete=models.CASCADE,
                                                  verbose_name='envío')

    class Meta:
        verbose_name = 'producto transferido'
        verbose_name_plural = 'productos transferidos'

    def __str__(self):
        return str(self.product)


class ProductTransferReception(models.Model):
    """
    The reception of a product transfer.
    """
    STATUS_CONFIRMED = 0
    STATUS_CANCELLED = 1
    STATUS_PENDING = 2
    STATUS_TYPES = (
        (STATUS_CONFIRMED, "Confirmada"),
        (STATUS_CANCELLED, "Cancelada"),
        (STATUS_PENDING, "Pendiente"),
    )

    sending_branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE,
                                       related_name='product_transfers_as_sending_branch',
                                       verbose_name='sucursal que envía')
    receiving_branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE,
                                         editable=False,
                                         related_name='product_transfers_as_receiving_branch',
                                         verbose_name='sucursal receptora')
    received_by_user = models.ForeignKey(Employee, on_delete=models.PROTECT, editable=False,
                                         related_name='received_product_transfers',
                                         verbose_name='recibido por')
    confirmed_by_user = models.ForeignKey(Employee, on_delete=models.PROTECT, editable=False, null=True,
                                          related_name='confirmed_product_receptions',
                                          verbose_name='confirmado por')
    date_received = models.DateTimeField(verbose_name='fecha de recepción')
    date_confirmed = models.DateTimeField(null=True, blank=True, editable=False, verbose_name='fecha de confirmación')
    status = models.PositiveSmallIntegerField(choices=STATUS_TYPES, default=STATUS_PENDING,
                                              verbose_name='estado')

    def confirm(self):
        """
        Confirms this product reception. It sets its status to CONFIRMED
        and adds the confirmed products to the inventory. The unconfirmed
        products are added as ProductRemovals.
        """
        useless_products = []
        inventory = None

        with transaction.atomic():
            self.status = ProductTransferReception.STATUS_CONFIRMED
            self.date_confirmed = datetime.datetime.now()
            self.save()

            for received_product in self.receivedproduct_set.all():
                inventory = self.receiving_branch.productsinventory
                inventory_item = inventory.productinventoryitem_set.filter(product=received_product.product).first()

                if not inventory_item:
                    inventory_item = ProductInventoryItem()
                    inventory_item.product = received_product.product
                    inventory_item.quantity = received_product.accepted_quantity
                else:
                    inventory_item.quantity += received_product.accepted_quantity

                inventory_item.save()

                if received_product.received_quantity != received_product.accepted_quantity:
                    useless_product_quantity = received_product.received_quantity - received_product.accepted_quantity

                    removed_product = RemovedProduct()
                    removed_product.product = received_product.product
                    removed_product.quantity = useless_product_quantity

                    useless_products.append(removed_product)

            if any(useless_products):
                product_removal = ProductRemoval()
                product_removal.cause = ProductRemoval.CAUSE_TRANSFER
                product_removal.product_transfer_reception = self
                product_removal.inventory = inventory
                product_removal.user = self.received_by_user
                product_removal.status = ProductRemoval.STATUS_CONFIRMED
                product_removal.removedproduct_set = useless_products
                product_removal.save()

    def get_confirm_params_for_ajax_request(self):
        """
        Returns a dictionary with the parameters necessary for the 'confirmOrCancelInventoryMovement'
        AJAX call.
        :return: A dictionary with the parameters.
        """
        url = reverse('productmovconfirmorcancel')
        model = self.__class__.__name__
        pk = self.pk
        action = 'confirm'

        return {'url': url, 'model': model, 'pk': pk, 'action': action}

    def cancel(self):
        """
        Cancels this product transfer shipment. Sets its status to CANCELLED
        and no products are removed from the inventory.
        """
        self.status = ProductTransferReception.STATUS_CANCELLED
        self.date_confirmed = datetime.datetime.now()
        self.save()

    def get_cancel_params_for_ajax_request(self):
        """
        Returns a dictionary with the parameters necessary for the 'confirmOrCancelInventoryMovement'
        AJAX call.
        :return: A dictionary with the parameters.
        """
        url = reverse('productmovconfirmorcancel')
        model = self.__class__.__name__
        pk = self.pk
        action = 'cancel'

        return {'url': url, 'model': model, 'pk': pk, 'action': action}

    class Meta:
        verbose_name = 'recepción de transferencia de productos'
        verbose_name_plural = 'recepciones de transferencias de productos'


class ReceivedProduct(models.Model):
    """
    The received and accepted quantity of a product
    received in product transfer.
    """
    REJECTION_QUANTITY_MISMATCH = 0
    REJECTION_MATERIAL_MISMATCH = 1
    REJECTION_POOR_CONDITION = 2
    REJECTION_REASONS = (
        (REJECTION_QUANTITY_MISMATCH, "La cantidad recibida no concuerda con la esperada."),
        (REJECTION_MATERIAL_MISMATCH, "El material recibido no concuerda con el esperado."),
        (REJECTION_MATERIAL_MISMATCH, "El material se encuentra en mal estado.")
    )

    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='producto')
    received_quantity = models.PositiveSmallIntegerField(default=1, verbose_name='cantidad recibida')
    accepted_quantity = models.PositiveSmallIntegerField(default=1, verbose_name='cantidad aceptada')
    product_transfer_reception = models.ForeignKey(ProductTransferReception, on_delete=models.CASCADE,
                                                   verbose_name='recepción')
    rejection_reason = models.PositiveSmallIntegerField(null=True, blank=True, choices=REJECTION_REASONS,
                                                        verbose_name='motivo de rechazo')

    class Meta:
        verbose_name = 'producto recibido'
        verbose_name_plural = 'productos recibidos'

    def __str__(self):
        return str(self.product)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.rejection_reason:
            self.accepted_quantity = self.received_quantity
        super(ReceivedProduct, self).save(force_insert, force_update, using, update_fields)


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
    inventory = models.ForeignKey(ProductsInventory, on_delete=models.PROTECT, editable=False,
                                  verbose_name='inventario')
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

    def save(self, **kwargs):
        if self.pk is not None:
            super(ReturnedProduct, self).save(**kwargs)
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
            super(ReturnedProduct, self).save(**kwargs)


class PurchaseOrder(models.Model):
    """
    A Purchase Order represents an entry of certain products
    given by a provider to a user's inventory.
    """

    STATUS_CONFIRMED = 0
    STATUS_CANCELLED = 1
    STATUS_PENDING = 2
    STATUS_TYPES = (
        (STATUS_CONFIRMED, "Confirmado"),
        (STATUS_CANCELLED, "Cancelado"),
        (STATUS_PENDING, "Pendiente"),
    )

    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, verbose_name='proveedor')
    date = models.DateTimeField(auto_now_add=True, verbose_name='fecha')
    invoice_folio = models.CharField(max_length=30, verbose_name='folio factura')
    branch_office = models.ForeignKey(BranchOffice, on_delete=models.CASCADE, editable=False, verbose_name='sucursal')
    status = models.PositiveSmallIntegerField(choices=STATUS_TYPES, default=STATUS_PENDING, verbose_name='estado')

    class Meta:
        verbose_name = 'orden de compra'
        verbose_name_plural = 'órdenes de compra'

    def __init__(self, *args, **kwargs):
        self.ajax_message_for_confirmation = ""
        self.ajax_message_for_cancellation = ""
        super(PurchaseOrder, self).__init__(*args, **kwargs)

    def __str__(self):
        return "P{0}".format(str(self.pk).zfill(9))

    @staticmethod
    def get_pending_purchase_orders_for_user(user: Employee):
        """
        Returns the set of product entries that are pending.
        :param user: The user for which the entries are needed.
        :return: A list with the product entries.
        """
        return PurchaseOrder.objects.filter(branch_office__administrator=user,
                                            status=PurchaseOrder.STATUS_PENDING)

    def get_absolute_url(self):
        """
        Returns the admin's change URL for this model.
        :return: The URL.
        """
        return reverse('admin:inventories_purchaseorder_change', args=[str(self.id)])

    def confirm(self):
        """
        Confirms a purchase order. Sets its status to
        CONFIRMED.
        """
        self.status = PurchaseOrder.STATUS_CONFIRMED
        self.save()

        self.ajax_message_for_confirmation = "Se confirmó la orden {0}.".format(str(self))

    def get_confirm_params_for_ajax_request(self):
        """
        Returns a dictionary with the parameters necessary for the 'confirmOrCancelInventoryMovement'
        AJAX call.
        :return: A dictionary with the parameters.
        """
        url = reverse('productmovconfirmorcancel')
        model = self.__class__.__name__
        pk = self.pk
        action = 'confirm'

        return {'url': url, 'model': model, 'pk': pk, 'action': action}

    def cancel(self):
        """
        Cancels a purchase order. Sets its status to
        CANCELLED.
        """
        self.status = PurchaseOrder.STATUS_CANCELLED
        self.save()

        self.ajax_message_for_cancellation = "Se canceló la orden {0}.".format(str(self))

    def get_cancel_params_for_ajax_request(self):
        """
        Returns a dictionary with the parameters necessary for the 'confirmOrCancelInventoryMovement'
        AJAX call.
        :return: A dictionary with the parameters.
        """
        url = reverse('productmovconfirmorcancel')
        model = self.__class__.__name__
        pk = self.pk
        action = 'cancel'

        return {'url': url, 'model': model, 'pk': pk, 'action': action}


class PurchasedProduct(models.Model):
    """
    A product belonging to a Purchase Order.
    """

    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='producto')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='cantidad')
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, verbose_name='orden de compra')

    class Meta:
        verbose_name = 'producto comprado'
        verbose_name_plural = 'productos comprados'

    def __str__(self):
        return str(self.product)


class ProductEntry(models.Model):
    """
    An addition of Product to a specific Inventory. It's related to a
    Purchase Order and a Provider.
    """

    STATUS_CONFIRMED = 0
    STATUS_CANCELLED = 1
    STATUS_PENDING = 2
    STATUS_TYPES = (
        (STATUS_CONFIRMED, "Confirmado"),
        (STATUS_CANCELLED, "Cancelado"),
        (STATUS_PENDING, "Pendiente"),
    )

    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT, verbose_name='orden de compra')
    inventory = models.ForeignKey(ProductsInventory, on_delete=models.PROTECT, verbose_name='inventario')
    date = models.DateTimeField(auto_now_add=True, verbose_name='fecha')
    status = models.PositiveSmallIntegerField(choices=STATUS_TYPES, default=STATUS_PENDING, verbose_name='estado')

    class Meta:
        verbose_name = 'ingreso de producto'
        verbose_name_plural = 'ingresos de producto'

    def __init__(self, *args, **kwargs):
        self.ajax_message_for_confirmation = ""
        self.ajax_message_for_cancellation = ""
        super(ProductEntry, self).__init__(*args, **kwargs)

    def __str__(self):
        return "Ingreso para orden de compra {0}".format(str(self.purchase_order))

    @staticmethod
    def get_pending_product_entries_for_user(user: Employee):
        """
        Returns the set of product entries that are pending.
        :param user: The user for which the entries are needed.
        :return: A list with the product entries.
        """
        return ProductEntry.objects.filter(inventory__supervisor=user,
                                           status=ProductEntry.STATUS_PENDING)

    def confirm(self):
        """
        Confirms this product entry. Sets the status as CONFIRMED and
        removes and adds the products to the inventory.
        """

        with transaction.atomic():
            self.status = ProductEntry.STATUS_CONFIRMED
            self.save()

            self.ajax_message_for_confirmation = "Se confirmó el ingreso para la orden {0}.\n".format(
                str(self.purchase_order))

            for entered_product in self.enteredproduct_set.all():
                inventory_item = self.inventory.productinventoryitem_set.filter(product=entered_product.product).first()

                if inventory_item is None:
                    inventory_item = ProductInventoryItem()
                    inventory_item.product = entered_product.product
                    inventory_item.quantity = entered_product.quantity

                    old_quantity = 0
                else:
                    old_quantity = inventory_item.quantity
                    inventory_item.quantity += entered_product.quantity

                new_quantity = inventory_item.quantity

                self.ajax_message_for_confirmation += "{0} [{1}] -> [{2}]\n".format(str(entered_product.product),
                                                                                    old_quantity, new_quantity)

                inventory_item.save()

    def get_confirm_params_for_ajax_request(self):
        """
        Returns a dictionary with the parameters necessary for the 'confirmOrCancelInventoryMovement'
        AJAX call.
        :return: A dictionary with the parameters.
        """
        url = reverse('productmovconfirmorcancel')
        model = self.__class__.__name__
        pk = self.pk
        action = 'confirm'

        return {'url': url, 'model': model, 'pk': pk, 'action': action}

    def cancel(self):
        """
        Cancels this product entry. Sets the status as CANCELLED.
        :return:
        """
        self.status = ProductEntry.STATUS_CANCELLED
        self.save()

        self.ajax_message_for_cancellation = "Ingreso para orden {0} cancelado.".format(str(self.purchase_order))

    def get_cancel_params_for_ajax_request(self):
        """
        Returns a dictionary with the parameters necessary for the 'confirmOrCancelInventoryMovement'
        AJAX call.
        :return: A dictionary with the parameters.
        """
        url = reverse('productmovconfirmorcancel')
        model = self.__class__.__name__
        pk = self.pk
        action = 'cancel'

        return {'url': url, 'model': model, 'pk': pk, 'action': action}

    def get_absolute_url(self):
        """
        Returns the admin's change URL for this model.
        :return: The URL.
        """
        return reverse('admin:inventories_productentry_change', args=[str(self.id)])


class EnteredProduct(models.Model):
    """
    The quantity of a Product that has been entered to an inventory
    through a Product Entry.
    """

    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='producto')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='cantidad')
    product_entry = models.ForeignKey(ProductEntry, on_delete=models.CASCADE, verbose_name='ingreso')

    class Meta:
        verbose_name = 'producto ingresado'
        verbose_name_plural = 'productos ingresados'

    def __str__(self):
        return str(self.product)


class ProductRemoval(models.Model):
    """
    A Product's removal from an inventory due to it being
    in bad conditions.
    """

    CAUSE_INTERNAL = 0
    CAUSE_PROVIDER = 1
    CAUSE_TRANSFER = 2
    CAUSE_TYPES = (
        (CAUSE_INTERNAL, "Interna"),
        (CAUSE_PROVIDER, "Proveedor"),
        (CAUSE_TRANSFER, "Transferencia"),
    )

    STATUS_CONFIRMED = 0
    STATUS_CANCELLED = 1
    STATUS_PENDING = 2
    STATUS_TYPES = (
        (STATUS_CONFIRMED, "Confirmada"),
        (STATUS_CANCELLED, "Cancelada"),
        (STATUS_PENDING, "Pendiente"),
    )

    cause = models.PositiveSmallIntegerField(choices=CAUSE_TYPES, default=CAUSE_INTERNAL, verbose_name='causa')
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, null=True, blank=True, verbose_name='proveedor')
    product_transfer_reception = models.ForeignKey(ProductTransferReception, on_delete=models.PROTECT, null=True,
                                                   blank=True,
                                                   verbose_name='recepción de transferencia de producto')
    inventory = models.ForeignKey(ProductsInventory, on_delete=models.PROTECT, verbose_name='inventario')
    date = models.DateTimeField(auto_now_add=True, verbose_name='fecha')
    user = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='usuario')
    status = models.PositiveSmallIntegerField(choices=STATUS_TYPES, default=STATUS_PENDING, verbose_name='estado')

    class Meta:
        verbose_name = 'merma de producto'
        verbose_name_plural = 'mermas de producto'

    def __init__(self, *args, **kwargs):
        self.ajax_message_for_confirmation = ""
        self.ajax_message_for_cancellation = ""
        super(ProductRemoval, self).__init__(*args, **kwargs)

    def __str__(self):
        return "{0} - {1}".format(str(self.inventory), str(self.user))

    @staticmethod
    def get_pending_product_removals_for_user(user: Employee):
        """
        Returns the set of product removals that are pending.
        :param user: The user for which the removals are needed.
        :return: A list with the product removals.
        """
        return ProductRemoval.objects.filter(inventory__supervisor=user,
                                             status=ProductRemoval.STATUS_PENDING)

    def get_absolute_url(self):
        """
        Returns the admin's change URL for this model.
        :return: The URL.
        """
        return reverse('admin:inventories_productremoval_change', args=[str(self.id)])

    def confirm(self):
        """
        Confirms this product removal. It sets its status to CONFIRMED
        and removes the products from the inventory.
        """
        with transaction.atomic():
            self.status = ProductRemoval.STATUS_CONFIRMED
            self.save()

            self.ajax_message_for_confirmation = "Se confirmó la merma {0}.\n".format(str(self))

            for removed_product in self.removedproduct_set.all():
                inventory_item = self.inventory.productinventoryitem_set.filter(product=removed_product.product)

                if inventory_item:
                    old_quantity = inventory_item.quantity

                    inventory_item.quantity -= removed_product.quantity
                    inventory_item.save()

                    new_quantity = inventory_item.quantity

                    self.ajax_message_for_confirmation += "{0} [{1}] -> [{2}]\n".format(str(removed_product.product),
                                                                                        old_quantity,
                                                                                        new_quantity)

    def get_confirm_params_for_ajax_request(self):
        """
        Returns a dictionary with the parameters necessary for the 'confirmOrCancelInventoryMovement'
        AJAX call.
        :return: A dictionary with the parameters.
        """
        url = reverse('productmovconfirmorcancel')
        model = self.__class__.__name__
        pk = self.pk
        action = 'confirm'

        return {'url': url, 'model': model, 'pk': pk, 'action': action}

    def cancel(self):
        """
        Cancels this product removal. Sets its status to CANCELLED.
        """
        self.status = ProductRemoval.STATUS_CANCELLED
        self.save()

    def get_cancel_params_for_ajax_request(self):
        """
        Returns a dictionary with the parameters necessary for the 'confirmOrCancelInventoryMovement'
        AJAX call.
        :return: A dictionary with the parameters.
        """
        url = reverse('productmovconfirmorcancel')
        model = self.__class__.__name__
        pk = self.pk
        action = 'cancel'

        return {'url': url, 'model': model, 'pk': pk, 'action': action}


class RemovedProduct(models.Model):
    """
    The quantity of a Product that has been removed from an inventory
    through a Product Removal.
    """

    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='producto')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='cantidad')
    product_removal = models.ForeignKey(ProductRemoval, on_delete=models.CASCADE, verbose_name='salida')

    class Meta:
        verbose_name = 'producto retirado'
        verbose_name_plural = 'productos retirados'

    def __str__(self):
        return str(self.product)


def string_to_model_class(string: str):
    """
    Returns the class belonging to this module
    that matches the given string.
    :param string: The class' name.
    :return: The class.
    """
    return getattr(sys.modules[__name__], string)
