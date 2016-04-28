import inventories.models as models
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from inventories.forms.product_definition_forms import AddOrChangeProductDefinitionForm


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


class InventoryAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the inventory entities.
    """
    filter_horizontal = ["items"]

    list_display = ('name', 'branch', 'supervisor', 'detail_page')

    def detail_page(self, obj):
        """

        :param obj:
        :return:
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


admin.site.register(models.ProductDefinition, ProductDefinitionAdmin)
admin.site.register(models.ProductInventoryItem)
admin.site.register(models.ProductsInventory, InventoryAdmin)
admin.site.register(models.MaterialDefinition)
admin.site.register(models.MaterialInventoryItem)
admin.site.register(models.MaterialsInventory, InventoryAdmin)
admin.site.register(models.ConsumableDefinition)
admin.site.register(models.ConsumableInventoryItem)
admin.site.register(models.ConsumablesInventory, InventoryAdmin)
admin.site.register(models.DurableGoodDefinition)
admin.site.register(models.DurableGoodsInventory, InventoryAdmin)
