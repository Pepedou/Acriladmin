import back_office.models as models
from django.contrib import admin


class OfficeBranchAdmin(admin.ModelAdmin):
    """
    Specifies the details for the admin app in regard
    to the OfficeBranch entity.
    """
    filter_horizontal = ("employees",)


admin.site.register(models.Address)
admin.site.register(models.PersonProfile)
admin.site.register(models.EmployeeRole)
admin.site.register(models.Employee)
admin.site.register(models.OrganizationProfile)
admin.site.register(models.Client)
admin.site.register(models.BranchOffice, OfficeBranchAdmin)
