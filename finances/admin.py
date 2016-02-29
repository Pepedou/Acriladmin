from django.contrib import admin
import finances.models as models


class OrderProductsInLine(admin.TabularInline):
    """
    Describes an inline class.
    """
    model = models.OrderProducts


class OrderServicesInLine(admin.TabularInline):
    """
    Describes an inline class.
    """
    model = models.OrderServices


class OrderAdmin(admin.ModelAdmin):
    """
    Contains the details for the admin app
    in regard to the Order entity.
    """
    inlines = [
        OrderProductsInLine,
        OrderServicesInLine
    ]


admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Invoice)
admin.site.register(models.ProductInvoice)
admin.site.register(models.ProductPrice)
admin.site.register(models.MaterialCost)
admin.site.register(models.ServiceInvoice)
admin.site.register(models.Transaction)
admin.site.register(models.RepairCost)
