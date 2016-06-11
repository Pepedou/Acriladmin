import finances.models as models
from django.contrib import admin
from django.db.models import Sum, F
from finances.forms.order_forms import AddOrChangeOrderForm
from finances.forms.productprice_forms import AddOrChangeProductPriceForm
from finances.forms.sale_forms import AddOrChangeSaleForm
from reversion.admin import VersionAdmin


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


class OrderAdmin(VersionAdmin):
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


class TransactionInline(admin.StackedInline):
    """
    Tabular inline for a Transaction used in the Invoice Admin.
    """
    model = models.Transaction


class InvoiceAdmin(VersionAdmin):
    """
    Contains the details for the admin app in regard to the Invoice entity.
    """
    list_display = ('id', 'is_closed',)
    readonly_fields = ('is_closed',)
    inlines = (TransactionInline,)


class ProductPriceAdmin(VersionAdmin):
    """
    Contains the details for the admin app in regard to the ProductPrice entity.
    """
    form = AddOrChangeProductPriceForm
    readonly_fields = ('authorized_by',)
    list_display = ('product', 'price', 'authorized_by',)
    list_filter = ('authorized_by',)

    def save_model(self, request, obj, form, change):
        """
        Overrides the default save function for the ProductPrice model. After each ProductPrice is saved,
        the authorized_by field is filled with the current user.
        """
        obj.authorized_by = request.user
        obj.save()


class MaterialCostAdmin(VersionAdmin):
    """
    Contains the details for the admin app in regard to the MaterialCost entity.
    """
    readonly_fields = ('authorized_by',)
    list_display = ('material', 'cost', 'authorized_by',)
    list_filter = ('authorized_by',)

    def save_model(self, request, obj, form, change):
        """
        Overrides the default save function for the MaterialCost model. After each MaterialCost is saved,
        the authorized_by field is filled with the current user.
        """
        obj.authorized_by = request.user
        obj.save()


class TransactionAdmin(VersionAdmin):
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


class RepairCostAdmin(VersionAdmin):
    """
    Contains the details for the admin app in regard to the RepairCost entity.
    """
    readonly_fields = ('authorized_by',)
    list_display = ('repair', 'cost', 'authorized_by',)
    list_filter = ('authorized_by',)

    def save_model(self, request, obj, form, change):
        """
        Overrides the default save function for the RepairCost model. After each RepairCost is saved,
        the authorized_by field is filled with the current user.
        """
        obj.authorized_by = request.user
        obj.save()


class SaleAdmin(VersionAdmin):
    """
    Contains the details for the admin app in regard to the Sale entity.
    """
    list_display = ['invoice', 'client', 'product', 'quantity']
    exclude = ['invoice']
    list_display_links = list_display
    list_filter = ('type', 'date', 'inventory',)
    form = AddOrChangeSaleForm

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ('product', 'quantity', 'order', 'inventory', 'client',
                    'amount', 'date',)
        else:
            return ['amount', 'date']


admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Invoice, InvoiceAdmin)
admin.site.register(models.ProductPrice, ProductPriceAdmin)
admin.site.register(models.MaterialCost, MaterialCostAdmin)
admin.site.register(models.Transaction, TransactionAdmin)
admin.site.register(models.RepairCost, RepairCostAdmin)
admin.site.register(models.Sale, SaleAdmin)
