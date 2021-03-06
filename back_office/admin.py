import logging

from cities_light.admin import CountryAdmin, CityAdmin, RegionAdmin
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.views.decorators.cache import never_cache
from reversion.admin import VersionAdmin

import back_office.models as models
from back_office.forms.employee_forms import AddOrChangeEmployeeForm
from inventories.models import ProductEntry, ProductRemoval, PurchaseOrder, ProductTransferShipment, \
    ProductTransferReception

db_logger = logging.getLogger('db')


class CustomAdminSite(AdminSite):
    """
    Custom Admin site. It's used to give extra content to the Index page.
    """

    @never_cache
    def index(self, request, extra_context=None):
        return super(CustomAdminSite, self).index(request, self.get_extra_content(request))

    def get_extra_content(self, request):
        """
        Returns additional content for the index context.
        :return: A dictionary with extra content for the index view.
        """
        user = request.user

        pending_items = self.get_pending_items(user)

        return {'pending_items': pending_items}

    @staticmethod
    def get_pending_items(user: models.Employee):
        """
        Returns a dictionary with the pending items
        for a user to review on its index page.
        :param user: The user for which the pending items are
        needed.
        :return: The dictionary with the pending items.
        """
        pending_items = {'pending_purchase_orders':
                             PurchaseOrder.get_pending_purchase_orders_for_user(user),
                         'pending_product_entries':
                             ProductEntry.get_pending_product_entries_for_user(user),
                         'pending_product_removals':
                             ProductRemoval.get_pending_product_removals_for_user(user),
                         'pending_product_transfer_shipments':
                             ProductTransferShipment.get_pending_product_transfer_shipments_for_user(
                                 user),
                         'pending_product_transfer_receptions':
                             ProductTransferReception.get_pending_product_transfer_receptions_for_user(
                                 user)}

        return pending_items


class AddressAdmin(VersionAdmin):
    """
    Specifies the details for the admin app in regard
    to the Address entity.
    """
    fields = [
        ('street', 'exterior_number'),
        'interior_number',
        'city',
        ('state', 'country'),
        'zip_code'
    ]
    list_display = ('street', 'exterior_number', 'city', 'state', 'country',)
    list_filter = ('country', 'state',)


class GroupInline(admin.StackedInline):
    """
    Admin inline for the many to many relationship
    between Employee and Group.
    """
    model = models.Employee.groups.through

    verbose_name = 'grupo'
    verbose_name_plural = 'grupos'


class GroupAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the Group entity.
    """
    inlines = [GroupInline]


class EmployeeAdmin(VersionAdmin, UserAdmin):
    """
    Specifies the details for the admin app in regard
    to the Employee entity.
    """
    form = AddOrChangeEmployeeForm
    fieldsets = UserAdmin.fieldsets + (
        ("Datos administrativos", {
            'fields': (
                'gender', 'phone', 'picture', 'address', 'branch_office',
            )
        },),
    )
    readonly_fields = ('password',)
    inlines = [GroupInline]

    def get_queryset(self, request):
        """
        Remove the root user from the list view.
        """
        return models.Employee.objects.exclude(username='root')


class BranchOfficeAdmin(VersionAdmin):
    """
    Specifies the details for the admin app in regard
    to the OfficeBranch entity.
    """
    list_display = ('name', 'administrator', 'phone',)
    list_display_links = list_display

    def save_related(self, request, form, formsets, change):
        """
        Overrides the save related method to add by default the administrator
        to the branch's employees if it's not already part of them.
        """
        try:
            super(BranchOfficeAdmin, self).save_related(request, form, formsets, change)

            branch_office = form.instance

            if branch_office.administrator not in branch_office.employees.all():
                branch_office.employees.add(branch_office.administrator)
        except Exception as e:
            db_logger.exception(e)
            raise


class CustomCountryAdmin(CountryAdmin):
    """
    Overrides the default admin for the Country entity.
    """

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class CustomRegionAdmin(RegionAdmin):
    """
    Overrides the default admin for the Region entity.
    """

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class CustomCityAdmin(CityAdmin):
    """
    Overrides the default admin for the City entity.
    """

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


admin_site = CustomAdminSite()

admin_site.register(models.Address, AddressAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(models.Employee, EmployeeAdmin)
admin_site.register(models.Client, VersionAdmin)
admin_site.register(models.BranchOffice, BranchOfficeAdmin)
admin_site.register(models.Country, CustomCountryAdmin)
admin_site.register(models.Region, CustomRegionAdmin)
admin_site.register(models.City, CustomCityAdmin)
admin_site.register(models.Provider)
