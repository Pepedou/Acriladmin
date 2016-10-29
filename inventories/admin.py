import logging

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.core.urlresolvers import reverse
from django.db import transaction
from django.utils.html import format_html
from reversion.admin import VersionAdmin

import inventories.models as models
from back_office.admin import admin_site
from inventories.forms.entered_product_forms import EnteredProductInlineForm
from inventories.forms.inventory_item_forms import TabularInLineConsumableInventoryItemForm, \
    TabularInLineMaterialInventoryItemForm, \
    TabularInLineDurableGoodInventoryItemForm
from inventories.forms.product_entry_forms import AddOrChangeProductEntryForm
from inventories.forms.product_forms import AddOrChangeProductForm
from inventories.forms.product_purchase_forms import PurchasedProductInlineForm
from inventories.forms.product_tabularinlines_forms import AddOrChangeProductComponentInlineForm
from inventories.forms.product_transfer_reception_forms import ReceivedProductInlineForm, \
    AddOrChangeProductTransferReceptionForm
from inventories.forms.product_transfer_reception_forms import ReceivedProductInlineFormset
from inventories.forms.product_transfer_shipment_forms import AddOrChangeProductTransferShipmentForm, \
    TransferredProductInlineForm, TransferredProductInlineFormset
from inventories.forms.productreimbursement_tabularinlines_forms import AddOrChangeReturnedProductTabularInlineForm
from inventories.forms.productremoval_forms import AddOrChangeProductRemovalForm
from inventories.forms.productsinventory_forms import AddOrChangeProductsInventoryForm
from inventories.forms.removedproduct_forms import RemovedProductForm, RemovedProductFormset

db_logger = logging.getLogger('db')


class ProductComponentInLine(admin.TabularInline):
    """
    Describes the inline render of a product component for the
    Product's admin view.
    """
    form = AddOrChangeProductComponentInlineForm
    model = models.ProductComponent


class ProductAdmin(VersionAdmin):
    """
    Specifies the details for the admin app in regard
    to the Product entity.
    """
    form = AddOrChangeProductForm
    inlines = [ProductComponentInLine]
    list_display = ['sku', 'description', 'line', 'length', 'width', 'thickness']
    list_display_links = ['sku', 'description']
    list_filter = ['is_composite', 'line', 'engraving']
    list_per_page = 50
    search_fields = ['sku', 'description']

    def save_model(self, request, obj, form, change):
        """
        Overrides the save method for the Product entity.
        It checks if the is_composite field is not selected and, if so,
        deletes all previously inserted product components.
        """
        super(ProductAdmin, self).save_model(request, obj, form, change)

        if not obj.is_composite:
            models.ProductComponent.objects.filter(product=obj).delete()


class InventoryItemAdmin(VersionAdmin):
    """
    Specifies the details for the admin app in regard
    to the ProductInventoryItem, MaterialInventoryItem,
    ConsumableInventoryItem and DurableGoodInventoryItem
    entities. It's main purpose is to override the
    'get_model_perms' method to hide those entities
    in the index view.
    """

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class ProductsInventoryAdmin(VersionAdmin):
    """
    Specifies the details for the admin app in regard
    to the inventory entities.
    """
    form = AddOrChangeProductsInventoryForm
    list_display = ('name', 'branch', 'supervisor', 'detail_page')
    readonly_fields = ('last_updater',)

    def detail_page(self, obj):
        """
        Returns the HTML code for the inventory's detail page.
        :param obj:The inventory.
        :return: The HTML code.
        """
        url = reverse('products_inventory', args=(obj.id,))

        return format_html('<a href="{}">Mostrar detalle</a>', url)

    detail_page.short_description = "Detalle"

    def save_model(self, request, obj, form, change):
        """
        Overrides the default save function for the ProductsInventory model. After each ProductsInventory is saved,
        the last_updater field is filled with the current user.
        """
        obj.last_updater = request.user

        super(ProductsInventoryAdmin, self).save_model(request, obj, form, change)


class MaterialInventoryItemInLine(admin.TabularInline):
    """
    Describes the inline render of a product inventory item
    for the MaterialInventoryItem's admin view.
    """
    form = TabularInLineMaterialInventoryItemForm
    model = models.MaterialInventoryItem


class MaterialsInventoryAdmin(VersionAdmin):
    """
    Specifies the details for the admin app in regard
    to the inventory entities.
    """
    list_display = ('name', 'branch', 'supervisor', 'detail_page')
    inlines = (MaterialInventoryItemInLine,)
    readonly_fields = ('last_updater',)

    def detail_page(self, obj):
        """
        Returns the HTML code for the inventory's detail page.
        :param obj:The inventory.
        :return: The HTML code.
        """
        url = reverse('materials_inventory', args=(obj.id,))

        return format_html('<a href="{}">Mostrar detalle</a>', url)

    detail_page.short_description = "Detalle"

    def save_model(self, request, obj, form, change):
        """
        Overrides the default save function for the MaterialsInventory model.
        After each MaterialsInventory is saved, the last_updater field is filled with the current user.
        """
        obj.last_updater = request.user
        super(MaterialsInventoryAdmin, self).save_model(request, obj, form, change)


class ConsumableInventoryItemInLine(admin.TabularInline):
    """
    Describes the inline render of a product inventory item
    for the ConsumableInventoryItem's admin view.
    """
    form = TabularInLineConsumableInventoryItemForm
    model = models.ConsumableInventoryItem


class ConsumablesInventoryAdmin(VersionAdmin):
    """
    Specifies the details for the admin app in regard
    to the inventory entities.
    """
    list_display = ('name', 'branch', 'supervisor', 'detail_page')
    inlines = (ConsumableInventoryItemInLine,)
    readonly_fields = ('last_updater',)

    def detail_page(self, obj):
        """
        Returns the HTML code for the inventory's detail page.
        :param obj:The inventory.
        :return: The HTML code.
        """
        url = reverse('consumables_inventory', args=(obj.id,))

        return format_html('<a href="{}">Mostrar detalle</a>', url)

    detail_page.short_description = "Detalle"

    def save_model(self, request, obj, form, change):
        """
        Overrides the default save function for the ConsumablesInventory model.
        After each ConsumablesInventory is saved, the last_updater field is filled with the current user.
        """
        obj.last_updater = request.user
        super(ConsumablesInventoryAdmin, self).save_model(request, obj, form, change)


class DurableGoodInventoryItemInLine(admin.TabularInline):
    """
    Describes the inline render of a product inventory item
    for the ProductInventoryItem's admin view.
    """
    form = TabularInLineDurableGoodInventoryItemForm
    model = models.DurableGoodInventoryItem


class DurableGoodsInventoryAdmin(VersionAdmin):
    """
    Specifies the details for the admin app in regard
    to the inventory entities.
    """
    list_display = ('name', 'branch', 'supervisor', 'detail_page')
    inlines = (DurableGoodInventoryItemInLine,)
    readonly_fields = ('last_updater',)

    def detail_page(self, obj):
        """
        Returns the HTML code for the inventory's detail page.
        :param obj:The inventory.
        :return: The HTML code.
        """
        url = reverse('durable_goods_inventory', args=(obj.id,))

        return format_html('<a href="{}">Mostrar detalle</a>', url)

    detail_page.short_description = "Detalle"

    def save_model(self, request, obj, form, change):
        """
        Overrides the default save function for the DurableGoodsInventory model.
        After each DurableGoodsInventory is saved,
        the last_updater field is filled with the current user.
        """
        obj.last_updater = request.user
        super(DurableGoodsInventoryAdmin, self).save_model(request, obj, form, change)


class TransferredProductInLine(admin.TabularInline):
    """
    Describes the inline render of a transferred product
    for the ProductTransferShipment's admin view.
    """
    model = models.TransferredProduct
    form = TransferredProductInlineForm
    formset = TransferredProductInlineFormset

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super(TransferredProductInLine, self).get_formset(request, obj, **kwargs)

        class FormsetWithRequest(formset_class):
            """Subclass to add request"""

            def __new__(cls, *args, **kwargs2):
                kwargs2['request'] = request
                return formset_class(*args, **kwargs2)

        return FormsetWithRequest

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status != models.ProductTransferShipment.STATUS_PENDING:
            return 'product', 'quantity',
        else:
            return []

    def get_extra(self, request, obj=None, **kwargs):
        if obj and obj.status != models.ProductTransferShipment.STATUS_PENDING:
            return 0
        else:
            return super(TransferredProductInLine, self).get_extra(request, obj, **kwargs)

    def has_change_permission(self, request, obj=None):
        if obj and obj.status != models.ProductTransferShipment.STATUS_PENDING:
            return False
        else:
            return super(TransferredProductInLine, self).has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status != models.ProductTransferShipment.STATUS_PENDING:
            return False
        else:
            return super(TransferredProductInLine, self).has_delete_permission(request, obj)


class ProductTransferShipmentAdmin(ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the ProductTransferShipment entity.
    """
    form = AddOrChangeProductTransferShipmentForm
    inlines = [TransferredProductInLine]
    readonly_fields = ('source_branch', 'shipped_by_user', 'confirmed_by_user', 'date_confirmed', 'status',)
    list_display = ('source_branch', 'target_branch', 'date_shipped', 'date_confirmed', 'status',)
    list_filter = ('source_branch', 'target_branch', 'date_shipped', 'status',)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and obj.status != models.ProductTransferShipment.STATUS_PENDING:
            return self.readonly_fields + ('target_branch', 'date_shipped',)
        else:
            return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.status != models.ProductTransferShipment.STATUS_PENDING:
            return False
        else:
            return True

    def get_form(self, request, obj=None, **kwargs):
        form_class = super(ProductTransferShipmentAdmin, self).get_form(request, obj, **kwargs)

        class FormClassWithRequest(form_class):
            """Subclass the form to pass the request."""

            def __new__(cls, *args, **kwargs2):
                kwargs2['request'] = request
                return form_class(*args, **kwargs2)

        return FormClassWithRequest

    def save_model(self, request, obj, form, change):
        obj.shipped_by_user = request.user
        obj.source_branch = request.user.branch_office
        super(ProductTransferShipmentAdmin, self).save_model(request, obj, form, change)


class ReceivedProductInLine(admin.TabularInline):
    """
    Describes the inline render of a Received product
    for the ProductTransferReception's admin view.
    """
    model = models.ReceivedProduct
    form = ReceivedProductInlineForm
    formset = ReceivedProductInlineFormset

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super(ReceivedProductInLine, self).get_formset(request, obj, **kwargs)

        class FormsetWithRequest(formset_class):
            """Subclass to add request"""

            def __new__(cls, *args, **kwargs2):
                kwargs2['request'] = request
                return formset_class(*args, **kwargs2)

        return FormsetWithRequest

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status != models.ProductTransferReception.STATUS_PENDING:
            return 'product', 'accepted_quantity', 'received_quantity', 'rejection_reason',
        else:
            return []

    def get_extra(self, request, obj=None, **kwargs):
        if obj and obj.status != models.ProductTransferReception.STATUS_PENDING:
            return 0
        else:
            return super(ReceivedProductInLine, self).get_extra(request, obj, **kwargs)

    def has_change_permission(self, request, obj=None):
        if obj and obj.status != models.ProductTransferReception.STATUS_PENDING:
            return False
        else:
            return super(ReceivedProductInLine, self).has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status != models.ProductTransferReception.STATUS_PENDING:
            return False
        else:
            return super(ReceivedProductInLine, self).has_delete_permission(request, obj)


class ProductTransferReceptionAdmin(ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the ProductTransferReception entity.
    """
    form = AddOrChangeProductTransferReceptionForm
    inlines = [ReceivedProductInLine]
    readonly_fields = ('confirmed_by_user', 'date_confirmed', 'status',)
    list_display = ('folio', 'product_transfer_shipment', 'date_received', 'date_confirmed', 'status',)
    list_filter = ('product_transfer_shipment', 'date_received', 'status',)

    def get_formsets_with_inlines(self, request, obj=None):
        if not obj:
            return []
        else:
            return super(ProductTransferReceptionAdmin, self).get_formsets_with_inlines(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and obj.status != models.ProductTransferReception.STATUS_PENDING:
            return self.readonly_fields + ('date_received', 'product_transfer_shipment',)
        else:
            return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.status != models.ProductTransferReception.STATUS_PENDING:
            return False
        else:
            return True

    def save_model(self, request, obj, form, change):
        obj.received_by_user = request.user

        if not change:
            with transaction.atomic():
                super(ProductTransferReceptionAdmin, self).save_model(request, obj, form, change)
                self.prefill_received_products_with_shipments_products(obj)
        else:
            super(ProductTransferReceptionAdmin, self).save_model(request, obj, form, change)

    @staticmethod
    def prefill_received_products_with_shipments_products(product_transfer_shipment):
        """
        Fills the ProductTransferReception received items set with the related
        product transfer shipment's transferred product set.
        :param product_transfer_shipment: The ProductTransferShipment.
        """
        try:
            transfer = product_transfer_shipment.product_transfer_shipment

            for transferred_product in transfer.transferredproduct_set.all():
                received_product = models.ReceivedProduct()
                received_product.product = transferred_product.product
                received_product.accepted_quantity = transferred_product.quantity
                received_product.received_quantity = transferred_product.quantity
                received_product.product_transfer_reception = product_transfer_shipment
                received_product.save()

                product_transfer_shipment.receivedproduct_set.add(received_product)
        except Exception as e:
            db_logger.exception(e)
            raise

    def get_form(self, request, obj=None, **kwargs):
        form_class = super(ProductTransferReceptionAdmin, self).get_form(request, obj, **kwargs)

        class FormWithRequest(form_class):
            """Subclass to add request"""

            def __new__(cls, *args, **kwargs2):
                kwargs2['request'] = request
                return form_class(*args, **kwargs2)

        return FormWithRequest


class ReturnedProductInLine(admin.TabularInline):
    """
    Describes the inline render of a returned product for the
    Product's admin view.
    """
    form = AddOrChangeReturnedProductTabularInlineForm
    model = models.ReturnedProduct

    def get_extra(self, request, obj=None, **kwargs):
        return 0 if obj is not None else 3

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ['product', 'quantity']
        else:
            return []

    def get_actions(self, request):
        actions = super(ReturnedProductInLine, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return obj is None


class ProductReimbursementAdmin(ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the ProductReimbursement entity.
    """
    inlines = [ReturnedProductInLine]
    list_display = ('folio', 'inventory', 'date', 'monetary_difference',)
    list_display_links = list_display
    list_filter = ('inventory', 'date',)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['monetary_difference']
        else:
            return ['date', 'inventory', 'monetary_difference', 'sale']

    def get_actions(self, request):
        actions = super(ProductReimbursementAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.inventory = request.user.branch_office.productsinventory
        super(ProductReimbursementAdmin, self).save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        """
        Overrides super's save_related method in order to calculate the monetary difference
        between the returned products and the exchanged products.
        """
        try:
            from finances.models import ProductPrice
            from functools import reduce

            super(ProductReimbursementAdmin, self).save_related(request, form, formsets, change)

            reimbursement = form.instance

            returned_products = models.ReturnedProduct.objects.filter(reimbursement=reimbursement).all()

            if returned_products.count() > 0:
                product_prices = ProductPrice.objects.filter(product__in=[item.product for item in returned_products])

                reimbursement.monetary_difference = reduce(lambda x, y: x + y,
                                                           [a.price * b.quantity for a in product_prices for b in
                                                            returned_products if
                                                            a.product == b.product])

                reimbursement.save()
        except Exception as e:
            db_logger.exception(e)
            raise


class PurchasedProductInLine(admin.TabularInline):
    """
    Describes the inline render of a purchased product for the
    PurchasedProduct's admin view.
    """
    form = PurchasedProductInlineForm
    model = models.PurchasedProduct

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status != models.PurchaseOrder.STATUS_PENDING:
            return 'product', 'quantity',
        else:
            return []

    def get_extra(self, request, obj=None, **kwargs):
        if obj and obj.status != models.PurchaseOrder.STATUS_PENDING:
            return 0
        else:
            return super(PurchasedProductInLine, self).get_extra(request, obj, **kwargs)

    def has_change_permission(self, request, obj=None):
        if obj and obj.status != models.PurchaseOrder.STATUS_PENDING:
            return False
        else:
            return super(PurchasedProductInLine, self).has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status != models.PurchaseOrder.STATUS_PENDING:
            return False
        else:
            return super(PurchasedProductInLine, self).has_delete_permission(request, obj)


class PurchaseOrderAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the PurchaseOrder entity.
    """

    inlines = [PurchasedProductInLine]
    list_display = ('date_purchased', 'branch_office', 'provider', 'status',)
    list_filter = ('branch_office', 'status', 'date_purchased',)
    readonly_fields = ('branch_office', 'status', 'date_purchased',)

    def save_model(self, request, obj, form, change):
        obj.branch_office = request.user.branch_office
        obj.purchased_by_user = request.user
        super(PurchaseOrderAdmin, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status != models.PurchaseOrder.STATUS_PENDING:
            return self.readonly_fields + ('provider', 'invoice_folio',)
        else:
            return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status != models.PurchaseOrder.STATUS_PENDING:
            return False
        else:
            return super(PurchaseOrderAdmin, self).has_delete_permission(request, obj)


class EnteredProductInLine(admin.TabularInline):
    """
    Describes the inline render of a entered product for the
    ProductEntry's admin view.
    """
    model = models.EnteredProduct
    form = EnteredProductInlineForm

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status != models.ProductEntry.STATUS_PENDING:
            return 'product', 'quantity',
        else:
            return []

    def get_extra(self, request, obj=None, **kwargs):
        if obj and obj.status != models.ProductEntry.STATUS_PENDING:
            return 0
        else:
            return super(EnteredProductInLine, self).get_extra(request, obj, **kwargs)

    def has_change_permission(self, request, obj=None):
        if obj and obj.status != models.ProductEntry.STATUS_PENDING:
            return False
        else:
            return super(EnteredProductInLine, self).has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status != models.ProductEntry.STATUS_PENDING:
            return False
        else:
            return super(EnteredProductInLine, self).has_delete_permission(request, obj)


class ProductEntryAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the ProductEntry entity.
    """
    form = AddOrChangeProductEntryForm
    inlines = [EnteredProductInLine]
    list_display = ('date_entered', 'inventory', 'purchase_order', 'status',)
    list_filter = ('inventory', 'status', 'date_entered',)
    readonly_fields = ('inventory', 'status', 'date_entered',)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status != models.ProductEntry.STATUS_PENDING:
            return self.readonly_fields + ('purchase_order',)
        else:
            return self.readonly_fields

    def save_model(self, request, obj, form, change):
        obj.entered_by_user = request.user
        obj.inventory = request.user.branch_office.productsinventory
        super(ProductEntryAdmin, self).save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status != models.ProductEntry.STATUS_PENDING:
            return False
        else:
            return super(ProductEntryAdmin, self).has_delete_permission(request, obj)


class RemovedProductInLine(admin.TabularInline):
    """
    Describes the inline render of a removed product for the
    ProductRemoval's admin view.
    """
    model = models.RemovedProduct
    form = RemovedProductForm
    formset = RemovedProductFormset

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super(RemovedProductInLine, self).get_formset(request, obj, **kwargs)

        class FormSetWithRequest(formset_class):
            def __new__(cls, *args, **child_kwargs):
                child_kwargs['request'] = request
                return formset_class(*args, **child_kwargs)

        return FormSetWithRequest

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status != models.ProductRemoval.STATUS_PENDING:
            return 'product', 'quantity',
        else:
            return []

    def get_extra(self, request, obj=None, **kwargs):
        if obj and obj.status != models.ProductRemoval.STATUS_PENDING:
            return 0
        else:
            return super(RemovedProductInLine, self).get_extra(request, obj, **kwargs)

    def has_change_permission(self, request, obj=None):
        if obj and obj.status != models.ProductRemoval.STATUS_PENDING:
            return False
        else:
            return super(RemovedProductInLine, self).has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status != models.ProductRemoval.STATUS_PENDING:
            return False
        else:
            return super(RemovedProductInLine, self).has_delete_permission(request, obj)


class ProductRemovalAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the ProductRemoval entity.
    """

    form = AddOrChangeProductRemovalForm
    inlines = [RemovedProductInLine]
    list_display = 'inventory', 'removed_by_user', 'cause', 'status', 'date_removed',
    list_filter = 'inventory', 'cause', 'status', 'date_removed',
    readonly_fields = 'inventory', 'status', 'removed_by_user', 'date_removed',

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status != models.ProductRemoval.STATUS_PENDING:
            return self.readonly_fields + ('cause', 'provider', 'product_transfer_reception',)
        else:
            return self.readonly_fields

    def save_model(self, request, obj, form, change):
        obj.removed_by_user = request.user
        obj.inventory = request.user.branch_office.productsinventory
        super(ProductRemovalAdmin, self).save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status != models.ProductRemoval.STATUS_PENDING:
            return False
        else:
            return super(ProductRemovalAdmin, self).has_delete_permission(request, obj)


admin_site.register(models.Product, ProductAdmin)
admin_site.register(models.ProductInventoryItem, InventoryItemAdmin)
admin_site.register(models.ProductsInventory, ProductsInventoryAdmin)
admin_site.register(models.ProductTransferShipment, ProductTransferShipmentAdmin)
admin_site.register(models.ProductTransferReception, ProductTransferReceptionAdmin)
admin_site.register(models.ProductReimbursement, ProductReimbursementAdmin)
admin_site.register(models.PurchaseOrder, PurchaseOrderAdmin)
admin_site.register(models.ProductEntry, ProductEntryAdmin)
admin_site.register(models.ProductRemoval, ProductRemovalAdmin)
