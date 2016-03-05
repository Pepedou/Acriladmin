import back_office.models as models
from django.contrib import admin


class AddressAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the Address entity.
    """
    fields = (
        ('interior_number', 'exterior_number'),
        'street',
        ('town', 'city'),
        ('state', 'country'),
        'zip_code'
    )
    list_display = ('town', 'street', 'exterior_number')
    list_filter = ('country', 'state', 'city', 'town')


class BranchOfficeAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the OfficeBranch entity.
    """
    filter_horizontal = ("employees",)


admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.PersonProfile)
admin.site.register(models.EmployeeRole)
admin.site.register(models.Employee)
admin.site.register(models.Client)
admin.site.register(models.BranchOffice, BranchOfficeAdmin)
