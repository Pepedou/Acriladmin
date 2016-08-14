from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import Sum, F
from reversion.admin import VersionAdmin

import finances.models as models
from back_office.models import EmployeeRole
from finances.forms.productprice_forms import AddOrChangeProductPriceForm
from finances.forms.sale_forms import AddOrChangeSaleForm, SaleProductItemInlineForm


class TransactionInline(admin.StackedInline):
    """
    Tabular inline for a Transaction used in the Invoice Admin.
    """
    model = models.Transaction

    def get_extra(self, request, obj=None, **kwargs):
        if obj is None:
            return super(TransactionInline, self).get_extra(request, obj, **kwargs)
        else:
            return 0


class InvoiceAdmin(admin.ModelAdmin):
    """
    Contains the details for the admin app in regard to the Invoice entity.
    """
    list_display = ('folio', 'total', 'is_closed',)
    inlines = (TransactionInline,)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ('is_closed', 'state',)

        if obj is None:
            return readonly_fields
        else:
            return readonly_fields + ('folio',)

    def save_model(self, request, obj, form, change):
        obj.state = models.Invoice.STATE_VALID
        super(InvoiceAdmin, self).save_model(request, obj, form, change)


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


class TransactionAdmin(admin.ModelAdmin):
    """
    Contains the details for the admin app in regard to the Transaction entity.
    """
    list_filter = ['datetime']

    def save_model(self, request, obj, form, change):
        """
        Overrides the default save function for the Transaction model. After each transaction is saved,
        its associated invoice will be marked as closed if the amount covered by all related transactions
        is equal or higher than the invoice's total amount.
        """
        obj.save()

        invoice = obj.invoice

        related_transactions_sum = models.Transaction.objects.filter(invoice=invoice).aggregate(
            sum=Sum(F('amount')))['sum']

        if related_transactions_sum >= invoice.total:
            invoice.is_closed = True
        else:
            invoice.is_closed = False

        invoice.save()

    def get_readonly_fields(self, request, obj=None):
        if not obj or request.user.roles.filter(name=EmployeeRole.ADMINISTRATOR).exists():
            return super(TransactionAdmin, self).get_readonly_fields(request, obj)

        return ['invoice', 'payed_by', 'datetime', 'amount']


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


class SaleProductItemInline(admin.TabularInline):
    """
    Tabular inline for a SaleProductItem used in the Sale Admin.
    """
    model = models.SaleProductItem
    form = SaleProductItemInlineForm

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and obj.state == models.Sale.STATE_CANCELLED:
            return 'product', 'quantity',
        else:
            return []

    def get_extra(self, request, obj=None, **kwargs):
        return 3 if obj is None else 0

    def has_delete_permission(self, request, obj=None):
        return obj is None or obj.state != models.Sale.STATE_CANCELLED


class SaleAdmin(ModelAdmin):
    """
    Contains the details for the admin app in regard to the Sale entity.
    """
    list_display = ['folio', 'client', 'state']
    list_display_links = list_display
    list_filter = ('type', 'state', 'date',)
    form = AddOrChangeSaleForm
    inlines = (SaleProductItemInline,)
    actions = ['cancel_sales']
    fieldsets = (
        ('Datos', {
            'fields': ('client', 'shipping_address', 'type', 'payment_method', 'state')
        }),
        ('Montos', {
            'fields': ('date', 'invoice', 'subtotal', 'shipping_and_handling',
                       'discount', 'total',),
        })
    )

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and obj.state == models.Sale.STATE_ACTIVE:
            return ('product', 'quantity', 'order', 'client',
                    'date', 'state', 'subtotal', 'total',)
        if obj is not None and obj.state == models.Sale.STATE_CANCELLED:
            return ('client', 'type', 'state', 'shipping_address', 'payment_method',
                    'product', 'quantity', 'invoice', 'date',
                    'subtotal', 'shipping_and_handling', 'discount', 'total',)
        else:
            return 'date', 'state', 'subtotal', 'total',

    def get_actions(self, request):
        actions = super(SaleAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.state == models.Sale.STATE_CANCELLED:
            return False
        else:
            return True

    def cancel_sales(self, request, queryset):
        """
        Cancels the requested sales.
        :param request: The received HTTP request.
        :param queryset: The sales to cancel.
        """
        num_failed_cancelations = 0
        num_successfull_cancelations = 0

        for sale in queryset:
            try:
                sale.cancel()
                num_successfull_cancelations += 1
            except:
                num_failed_cancelations += 1

        if num_failed_cancelations:
            message = "Ocurrió un error al cancelar {0} ventas. Recargue la página para ver cuáles.".format(
                num_failed_cancelations)
        else:
            message = "Se cancelaron exitosamente {0} ventas.".format(num_successfull_cancelations)

        self.message_user(request, message)

    cancel_sales.short_description = "Cancelar las ventas elegidas"

    def save_model(self, request, obj, form, change):
        obj.inventory = request.user.branch_office.productsinventory
        obj.save()

    def save_related(self, request, form, formsets, change):
        obj = form.instance
        super(SaleAdmin, self).save_related(request, form, formsets, change)
        obj.invoice.state = models.Invoice.STATE_VALID
        obj.invoice.save()


admin.site.register(models.Invoice, InvoiceAdmin)
admin.site.register(models.ProductPrice, ProductPriceAdmin)
admin.site.register(models.MaterialCost, MaterialCostAdmin)
admin.site.register(models.Transaction, TransactionAdmin)
admin.site.register(models.RepairCost, RepairCostAdmin)
admin.site.register(models.Sale, SaleAdmin)
