from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from reversion.admin import VersionAdmin

import inventories.models as models
from back_office.admin import admin_site
from inventories.forms.inventory_item_forms import TabularInLineConsumableInventoryItemForm, \
    TabularInLineMaterialInventoryItemForm, \
    TabularInLineDurableGoodInventoryItemForm
from inventories.forms.product_forms import AddOrChangeProductForm
from inventories.forms.product_tabularinlines_forms import AddOrChangeProductComponentInlineForm
from inventories.forms.product_transfer_forms import AddOrChangeProductTransferForm
from inventories.forms.productreimbursement_tabularinlines_forms import AddOrChangeReturnedProductTabularInlineForm
from inventories.forms.productremoval_forms import AddOrChangeProductRemovalForm
from inventories.forms.productsinventory_forms import AddOrChangeProductsInventoryForm
from inventories.forms.removedproduct_forms import RemovedProductForm, RemovedProductFormset


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
        obj.save()

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

        obj.save()


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
        obj.save()


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
        obj.save()


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
        obj.save()


class ProductTransferAdmin(ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the ProductTransfer entity.
    """
    form = AddOrChangeProductTransferForm
    list_display = (
        'source_branch', 'target_branch', 'product', 'quantity', 'is_confirmed', 'date_created', 'date_reviewed',)

    readonly_fields = ("product", "target_branch", "quantity",)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return 'is_confirmed', 'rejection_reason', 'confirmed_quantity', 'source_branch',
        elif request.user != obj.target_branch.productsinventory.supervisor and not request.user.is_superuser \
                or obj.is_confirmed:
            return self.readonly_fields + ('is_confirmed', 'rejection_reason', 'confirmed_quantity', 'source_branch',)
        elif obj.rejection_reason is None:
            return self.readonly_fields + ('source_branch',)
        else:
            return self.readonly_fields + ('is_confirmed', 'rejection_reason', 'confirmed_quantity', 'source_branch',)

    def get_actions(self, request):
        actions = super(ProductTransferAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.transfer_has_been_made:
            return False
        else:
            return True

    def get_form(self, request, obj=None, **kwargs):
        admin_form_class = super(ProductTransferAdmin, self).get_form(request, obj, **kwargs)

        class AdminFormWithRequest(admin_form_class):
            """Subclass to add request"""

            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return admin_form_class(*args, **kwargs)

        return AdminFormWithRequest

    def save_model(self, request, obj, form, change):
        obj.source_branch = request.user.branch_office
        obj.save()


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
        obj.save()

    def save_related(self, request, form, formsets, change):
        """
        Overrides super's save_related method in order to calculate the monetary difference
        between the returned products and the exchanged products.
        """
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


class PurchasedProductInLine(admin.TabularInline):
    """
    Describes the inline render of a purchased product for the
    PurchasedProduct's admin view.
    """
    model = models.PurchasedProduct


class PurchaseOrderAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the PurchaseOrder entity.
    """

    inlines = [PurchasedProductInLine]
    readonly_fields = ('branch_office', 'status', 'date',)

    def save_model(self, request, obj, form, change):
        obj.branch_office = request.user.branch_office
        super(PurchaseOrderAdmin, self).save_model(request, obj, form, change)


class EnteredProductInLine(admin.TabularInline):
    """
    Describes the inline render of a entered product for the
    ProductEntry's admin view.
    """
    model = models.EnteredProduct


class ProductEntryAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the ProductEntry entity.
    """

    inlines = [EnteredProductInLine]
    readonly_fields = ('inventory', 'status', 'date',)

    def save_model(self, request, obj, form, change):
        obj.inventory = request.user.branch_office.productsinventory
        super(ProductEntryAdmin, self).save_model(request, obj, form, change)


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


class ProductRemovalAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the ProductRemoval entity.
    """

    form = AddOrChangeProductRemovalForm
    inlines = [RemovedProductInLine]
    list_display = 'inventory', 'user', 'cause', 'status', 'date',
    list_filter = 'inventory', 'cause', 'status', 'date',
    readonly_fields = 'inventory', 'status', 'user', 'date',

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status != models.ProductRemoval.STATUS_PENDING:
            return self.readonly_fields + 'cause', 'provider', 'product_transfer',
        else:
            return self.readonly_fields

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.inventory = request.user.branch_office.productsinventory
        super(ProductRemovalAdmin, self).save_model(request, obj, form, change)


admin_site.register(models.Product, ProductAdmin)
admin_site.register(models.ProductInventoryItem, InventoryItemAdmin)
admin_site.register(models.ProductsInventory, ProductsInventoryAdmin)
admin_site.register(models.ProductTransfer, ProductTransferAdmin)
admin_site.register(models.ProductReimbursement, ProductReimbursementAdmin)
admin_site.register(models.PurchaseOrder, PurchaseOrderAdmin)
admin_site.register(models.ProductEntry, ProductEntryAdmin)
admin_site.register(models.ProductRemoval, ProductRemovalAdmin)
