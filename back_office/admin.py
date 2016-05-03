import back_office.models as models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from reversion.admin import VersionAdmin


# class EmployeeInLine(admin.StackedInline):
#     """
#
#     """
#     model = models.Employee
#
#
# class UserAdmin(BaseUserAdmin):
#     """
#     Specifies the details for the admin app in regard
#     to the User entity.
#     """
#     inlines = (EmployeeInLine,)


class AddressAdmin(VersionAdmin):
    """
    Specifies the details for the admin app in regard
    to the Address entity.
    """
    fields = (
        ('street', 'exterior_number'),
        'interior_number',
        ('town', 'city'),
        ('state', 'country'),
        'zip_code'
    )
    list_display = ('town', 'street', 'exterior_number')
    list_filter = ('country', 'state', 'city', 'town')


class EmployeeAdmin(VersionAdmin, UserAdmin):
    """
    Specifies the details for the admin app in regard
    to the Employee entity.
    """
    fieldsets = UserAdmin.fieldsets + (
        ("Datos administrativos", {
            'fields': (
                'gender', 'phone', 'picture', 'address', 'roles',
            )
        },),
    )


class BranchOfficeAdmin(VersionAdmin):
    """
    Specifies the details for the admin app in regard
    to the OfficeBranch entity.
    """
    filter_horizontal = ("employees",)


admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.EmployeeRole, VersionAdmin)
admin.site.register(models.Employee, EmployeeAdmin)
admin.site.register(models.Client, VersionAdmin)
admin.site.register(models.BranchOffice, BranchOfficeAdmin)
