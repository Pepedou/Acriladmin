import inventories.models as models
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from inventories.forms.product_definition_forms import AddOrChangeProductDefinitionForm
from inventories.forms.product_inventory_item_forms import TabularInLineProductInventoryItemForm
from inventories.forms.product_transfer_forms import AddOrChangeProductTransferForm


class ProductComponentInLine(admin.TabularInline):
    """
    Describes the inline render of a product component for the
    ProductDefinition's admin view.
    """
    model = models.ProductComponent


class ProductDefinitionAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the ProductDefinition entity.
    """
    form = AddOrChangeProductDefinitionForm
    inlines = [ProductComponentInLine]

    def save_model(self, request, obj, form, change):
        """
        Overrides the save method for the ProductDefinition entity.
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


class InventoryAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the inventory entities.
    """
    list_display = ('name', 'branch', 'supervisor', 'detail_page')

    def detail_page(self, obj):
        """
        Returns the HTML code for the inventory's detail page.
        :param obj:The inventory.
        :return: The HTML code.
        """
        url = None
        if isinstance(obj, models.ProductsInventory):
            url = reverse('products_inventory', args=(obj.id,))
        elif isinstance(obj, models.MaterialsInventory):
            url = reverse('materials_inventory', args=(obj.id,))
        elif isinstance(obj, models.ConsumablesInventory):
            url = reverse('consumables_inventory', args=(obj.id,))
        elif isinstance(obj, models.DurableGoodsInventory):
            url = reverse('durable_goods_inventory', args=(obj.id,))

        return format_html('<a href="{}">Mostrar detalle</a>', url)

    detail_page.short_description = "Detalle"


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


class ProductTransferAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the ProductTransfer entity.
    """
    form = AddOrChangeProductTransferForm

    readonly_fields = ("product", "source_branch", "target_branch", "quantity",)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return super(ProductTransferAdmin, self).get_readonly_fields(request, obj)
        else:
            return tuple()


admin.site.register(models.ProductDefinition, ProductDefinitionAdmin)
admin.site.register(models.ProductInventoryItem, InventoryItemAdmin)
admin.site.register(models.ProductsInventory, ProductsInventoryAdmin)
admin.site.register(models.MaterialDefinition)
admin.site.register(models.MaterialInventoryItem, InventoryItemAdmin)
admin.site.register(models.MaterialsInventory, InventoryAdmin)
admin.site.register(models.ConsumableDefinition)
admin.site.register(models.ConsumableInventoryItem, InventoryItemAdmin)
admin.site.register(models.ConsumablesInventory, InventoryAdmin)
admin.site.register(models.DurableGoodDefinition)
admin.site.register(models.DurableGoodInventoryItem, InventoryItemAdmin)
admin.site.register(models.DurableGoodsInventory, InventoryAdmin)
admin.site.register(models.ProductTransfer, ProductTransferAdmin)
