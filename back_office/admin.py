import back_office.models as models
from back_office.forms.employee_forms import AddOrChangeEmployeeForm
from cities_light.admin import CountryAdmin, CityAdmin, RegionAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from reversion.admin import VersionAdmin


class AddressAdmin(VersionAdmin):
    """
    Specifies the details for the admin app in regard
    to the Address entity.
    """
    fields = (
        ('street', 'exterior_number'),
        'interior_number',
        ('city'),
        ('state', 'country'),
        'zip_code'
    )
    list_display = ('street', 'exterior_number')
    list_filter = ('country', 'state', 'city',)


class RoleInline(admin.StackedInline):
    """

    """
    model = models.Employee.roles.through

    verbose_name = 'rol'
    verbose_name_plural = 'roles'


class EmployeeRoleAdmin(admin.ModelAdmin):
    inlines = [RoleInline]


class EmployeeAdmin(VersionAdmin, UserAdmin):
    """
    Specifies the details for the admin app in regard
    to the Employee entity.
    """
    form = AddOrChangeEmployeeForm
    fieldsets = UserAdmin.fieldsets + (
        ("Datos administrativos", {
            'fields': (
                'gender', 'phone', 'picture', 'address',
            )
        },),
    )
    inlines = [RoleInline]


class BranchOfficeAdmin(VersionAdmin):
    """
    Specifies the details for the admin app in regard
    to the OfficeBranch entity.
    """
    filter_horizontal = ("employees",)


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


admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.EmployeeRole, EmployeeRoleAdmin)
admin.site.register(models.Employee, EmployeeAdmin)
admin.site.register(models.Client, VersionAdmin)
admin.site.register(models.BranchOffice, BranchOfficeAdmin)
admin.site.unregister(models.Country)
admin.site.register(models.Country, CustomCountryAdmin)
admin.site.unregister(models.Region)
admin.site.register(models.Region, CustomRegionAdmin)
admin.site.unregister(models.City)
admin.site.register(models.City, CustomCityAdmin)
