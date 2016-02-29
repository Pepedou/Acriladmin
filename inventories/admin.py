from django.contrib import admin
import inventories.models as models


class InventoryAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the inventory entities.
    """
    filter_horizontal = ["items"]


admin.site.register(models.ProductDefinition)
admin.site.register(models.Product)
admin.site.register(models.ProductComponent)
admin.site.register(models.ProductsInventory, InventoryAdmin)
admin.site.register(models.MaterialDefinition)
admin.site.register(models.Material)
admin.site.register(models.MaterialsInventory, InventoryAdmin)
admin.site.register(models.ConsumableDefinition)
admin.site.register(models.Consumable)
admin.site.register(models.ConsumablesInventory, InventoryAdmin)
admin.site.register(models.DurableGoodDefinition)
admin.site.register(models.DurableGoodsInventory, InventoryAdmin)
admin.site.register(models.Movement)
