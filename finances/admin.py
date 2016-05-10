import finances.models as models
from django.contrib import admin
from django.db.models import Sum, F
from finances.forms.order_forms import AddOrChangeOrderForm
from finances.forms.productprice_forms import AddOrChangeProductPriceForm


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
    fieldsets = (
        ("Datos administrativos", {
            'fields': ('status', 'target', 'client', 'date',)
        }),
        ("Cotización", {
            'fields': ('subtotal', 'shipping_and_handling', 'discount', 'total',)
        }),
        ("Otros", {
            'fields': ('project',)
        })
    )

    # noinspection PyMethodMayBeStatic


class InvoiceAdmin(admin.ModelAdmin):
    """
    Contains the details for the admin app in regard to the Invoice entity.
    """
    list_display = ('id', 'is_closed',)
    readonly_fields = ('is_closed',)


class ProductPriceAdmin(admin.ModelAdmin):
    """
    Contains the details for the admin app in regard to the ProductPrice entity.
    """
    form = AddOrChangeProductPriceForm
    readonly_fields = ('authorized_by',)

    def save_model(self, request, obj, form, change):
        """
        Overrides the default save function for the ProductPrice model. After each ProductPrice is saved,
        the authorized_by field is filled with the current user.
        """
        obj.authorized_by = request.user
        obj.save()


class MaterialCostAdmin(admin.ModelAdmin):
    """
    Contains the details for the admin app in regard to the MaterialCost entity.
    """
    readonly_fields = ('authorized_by',)

    def save_model(self, request, obj, form, change):
        """
        Overrides the default save function for the MaterialCost model. After each MaterialCost is saved,
        the authorized_by field is filled with the current user.
        """
        obj.authorized_by = request.user
        obj.save()


class TransactionAdmin(admin.ModelAdmin):
    """
    Contains the details for the admin app in regard to the Transaction entity.
    """

    def save_model(self, request, obj, form, change):
        """
        Overrides the default save function for the Transaction model. After each transaction is saved,
        its associated invoice will be marked as closed if the amount covered by all related transactions
        is equal or higher than the invoice's total amount.
        """
        obj.save()

        invoice = obj.invoice

        related_transactions_sum = models.Transaction.objects.filter(invoice_id=invoice.id).aggregate(
            sum=Sum(F('amount')))['sum']

        if related_transactions_sum >= invoice.total:
            invoice.is_closed = True
        else:
            invoice.is_closed = False

        invoice.save()


class RepairCostAdmin(admin.ModelAdmin):
    """
    Contains the details for the admin app in regard to the RepairCost entity.
    """
    readonly_fields = ('authorized_by',)

    def save_model(self, request, obj, form, change):
        """
        Overrides the default save function for the RepairCost model. After each RepairCost is saved,
        the authorized_by field is filled with the current user.
        """
        obj.authorized_by = request.user
        obj.save()


class SaleAdmin(admin.ModelAdmin):
    """
    Contains the details for the admin app in regard to the Sale entity.
    """
    list_display = ['invoice', 'client', 'product', 'quantity']
    exclude = ['invoice']
    list_display_links = list_display


admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Invoice, InvoiceAdmin)
admin.site.register(models.ProductPrice, ProductPriceAdmin)
admin.site.register(models.MaterialCost, MaterialCostAdmin)
admin.site.register(models.Transaction, TransactionAdmin)
admin.site.register(models.RepairCost, RepairCostAdmin)
admin.site.register(models.Sale, SaleAdmin)
