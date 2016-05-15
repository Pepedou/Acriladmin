import inventories.models as models
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from inventories.forms.inventory_item_forms import TabularInLineProductInventoryItemForm, \
    TabularInLineConsumableInventoryItemForm, TabularInLineMaterialInventoryItemForm, \
    TabularInLineDurableGoodInventoryItemForm
from inventories.forms.product_forms import AddOrChangeProductForm
from inventories.forms.product_reimbursement_inlines_forms import AddOrChangeExchangedProductForm, \
    AddOrChangeReturnedProductForm
from inventories.forms.product_transfer_forms import AddOrChangeProductTransferForm


class ProductComponentInLine(admin.TabularInline):
    """
    Describes the inline render of a product component for the
    Product's admin view.
    """
    model = models.ProductComponent


class ProductAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the Product entity.
    """
    form = AddOrChangeProductForm
    inlines = [ProductComponentInLine]
    list_display = ['sku', 'description', 'line', 'length', 'width', 'thickness']
    list_display_links = ['sku', 'description']
    list_filter = ['line', 'color', 'engraving', 'is_composite']
    search_fields = ['sku', 'description']

    def save_model(self, request, obj, form, change):
        """
        Overrides the save method for the Product entity.
        It checks if the is_composite field is not selected and, if so,
        deletes all previously inserted product components.
        """
        obj.save()

        if not obj.is_composite:
            models.ProductComponent.objects.filter(product_id=obj.sku).delete()


class InventoryItemAdmin(admin.ModelAdmin):
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


class ProductInventoryItemInLine(admin.TabularInline):
    """
    Describes the inline render of a product inventory item
    for the ProductInventoryItem's admin view.
    """
    form = TabularInLineProductInventoryItemForm
    model = models.ProductInventoryItem


class ProductsInventoryAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the inventory entities.
    """
    list_display = ('name', 'branch', 'supervisor', 'detail_page')
    inlines = (ProductInventoryItemInLine,)

    def detail_page(self, obj):
        """
        Returns the HTML code for the inventory's detail page.
        :param obj:The inventory.
        :return: The HTML code.
        """
        url = reverse('products_inventory', args=(obj.id,))

        return format_html('<a href="{}">Mostrar detalle</a>', url)

    detail_page.short_description = "Detalle"


class MaterialInventoryItemInLine(admin.TabularInline):
    """
    Describes the inline render of a product inventory item
    for the MaterialInventoryItem's admin view.
    """
    form = TabularInLineMaterialInventoryItemForm
    model = models.MaterialInventoryItem


class MaterialInventoryAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the inventory entities.
    """
    list_display = ('name', 'branch', 'supervisor', 'detail_page')
    inlines = (MaterialInventoryItemInLine,)

    def detail_page(self, obj):
        """
        Returns the HTML code for the inventory's detail page.
        :param obj:The inventory.
        :return: The HTML code.
        """
        url = reverse('materials_inventory', args=(obj.id,))

        return format_html('<a href="{}">Mostrar detalle</a>', url)

    detail_page.short_description = "Detalle"


class ConsumableInventoryItemInLine(admin.TabularInline):
    """
    Describes the inline render of a product inventory item
    for the ConsumableInventoryItem's admin view.
    """
    form = TabularInLineConsumableInventoryItemForm
    model = models.ConsumableInventoryItem


class ConsumableInventoryAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the inventory entities.
    """
    list_display = ('name', 'branch', 'supervisor', 'detail_page')
    inlines = (ConsumableInventoryItemInLine,)

    def detail_page(self, obj):
        """
        Returns the HTML code for the inventory's detail page.
        :param obj:The inventory.
        :return: The HTML code.
        """
        url = reverse('consumables_inventory', args=(obj.id,))

        return format_html('<a href="{}">Mostrar detalle</a>', url)

    detail_page.short_description = "Detalle"


class DurableGoodInventoryItemInLine(admin.TabularInline):
    """
    Describes the inline render of a product inventory item
    for the ProductInventoryItem's admin view.
    """
    form = TabularInLineDurableGoodInventoryItemForm
    model = models.DurableGoodInventoryItem


class DurableGoodInventoryAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the inventory entities.
    """
    list_display = ('name', 'branch', 'supervisor', 'detail_page')
    inlines = (DurableGoodInventoryItemInLine,)

    def detail_page(self, obj):
        """
        Returns the HTML code for the inventory's detail page.
        :param obj:The inventory.
        :return: The HTML code.
        """
        url = reverse('durable_goods_inventory', args=(obj.id,))

        return format_html('<a href="{}">Mostrar detalle</a>', url)

    detail_page.short_description = "Detalle"


class ProductTransferAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the ProductTransfer entity.
    """
    form = AddOrChangeProductTransferForm
    list_display = ('source_branch', 'target_branch', 'product', 'quantity', 'is_confirmed',)

    readonly_fields = ("product", "source_branch", "target_branch", "quantity",)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            if request.user == obj.target_branch.productsinventory.supervisor or request.user.is_superuser \
                    and obj.is_confirmed is False:
                return super(ProductTransferAdmin, self).get_readonly_fields(request, obj)
            else:
                return super(ProductTransferAdmin, self).get_readonly_fields(request, obj) + ('is_confirmed',)
        else:
            return 'is_confirmed',


class ReturnedProductInLine(admin.TabularInline):
    """
    Describes the inline render of a returned product for the
    Product's admin view.
    """
    form = AddOrChangeReturnedProductForm
    model = models.ReturnedProduct


class ExchangedProductInLine(admin.TabularInline):
    """
    Describes the inline render of a returned product for the
    Product's admin view.
    """
    form = AddOrChangeExchangedProductForm
    model = models.ExchangedProduct


class ProductReimbursementAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the ProductReimbursement entity.
    """
    inlines = [ReturnedProductInLine, ExchangedProductInLine]
    readonly_fields = ('monetary_difference',)


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductInventoryItem, InventoryItemAdmin)
admin.site.register(models.ProductsInventory, ProductsInventoryAdmin)
admin.site.register(models.Material)
admin.site.register(models.MaterialInventoryItem, InventoryItemAdmin)
admin.site.register(models.MaterialsInventory, MaterialInventoryAdmin)
admin.site.register(models.Consumable)
admin.site.register(models.ConsumableInventoryItem, InventoryItemAdmin)
admin.site.register(models.ConsumablesInventory, ConsumableInventoryAdmin)
admin.site.register(models.DurableGood)
admin.site.register(models.DurableGoodInventoryItem, InventoryItemAdmin)
admin.site.register(models.DurableGoodsInventory, DurableGoodInventoryAdmin)
admin.site.register(models.ProductTransfer, ProductTransferAdmin)
admin.site.register(models.ProductReimbursement, ProductReimbursementAdmin)
