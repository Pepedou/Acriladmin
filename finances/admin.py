import finances.models as models
from django.contrib import admin
from finances.forms.order_forms import AddOrChangeOrderForm


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
    form = AddOrChangeOrderForm
    inlines = [
        OrderProductsInLine,
        OrderServicesInLine
    ]
    readonly_fields = [
        'total'
    ]


# noinspection PyMethodMayBeStatic
class InvoiceAdmin(admin.ModelAdmin):
    """
    Contains the details for the admin app
    in regard to the Invoice entity.
    """
    list_display = ('id', 'get_order_client', 'get_order_client_address',)
    search_fields = ('id', 'order__client__name', 'order__client__address__street')
    list_filter = ('order__client__name',)

    def get_order_client(self, obj):
        return obj.order.client

    get_order_client.short_description = 'Cliente'

    def get_order_client_address(self, obj):
        return obj.order.client.address

    get_order_client_address.short_description = 'Dirección'


admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Invoice, InvoiceAdmin)
admin.site.register(models.ProductInvoice)
admin.site.register(models.ProductPrice)
admin.site.register(models.MaterialCost)
admin.site.register(models.ServiceInvoice)
admin.site.register(models.Transaction)
admin.site.register(models.RepairCost)
