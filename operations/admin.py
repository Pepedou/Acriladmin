from django.contrib import admin
from reversion.admin import VersionAdmin

import operations.models as models
from back_office.admin import admin_site
from operations.forms.project_forms import AddOrChangeProjectForm
from operations.forms.project_materials_inline_forms import ProjectMaterialsInLineForm
from operations.forms.project_products_inline_forms import ProjectProductsInLineForm


class ProjectProductsInLine(admin.TabularInline):
    """
    Tabular inline for the Products shown in the Project admin page.
    """
    model = models.ProjectProductsEntry
    form = ProjectProductsInLineForm

    verbose_name = 'producto'
    verbose_name_plural = 'productos utilizados'


class ProjectMaterialsInLine(admin.TabularInline):
    """
    Tabular inline for the Materials shown in the Project admin page.
    """
    model = models.ProjectMaterialsEntry
    form = ProjectMaterialsInLineForm

    verbose_name = 'material'
    verbose_name_plural = 'materiales utilizados'


class ProjectAdmin(VersionAdmin):
    """
    Specifies the details for the admin app in regard
    to the ProjectAdmin entity.
    """
    form = AddOrChangeProjectForm
    fieldsets = (
        ("Datos administrativos", {
            'fields': ('name', 'description', 'supervisor', 'client', 'sales_agent',
                       'start_date', 'end_date')
        }),
        ("Datos operativos", {
            'fields': ('vehicle', 'has_been_paid', 'cost', 'amount_paid', 'transactions',)
        }),
    )
    filter_horizontal = ('transactions',)
    inlines = [
        ProjectProductsInLine,
        ProjectMaterialsInLine,
    ]


class ProjectEstimationProductsInLine(admin.TabularInline):
    """
    Tabular inline for the Products shown in the Project Estimation
    admin page.
    """
    model = models.ProjectEstimationProductsEntry

    verbose_name = 'producto'
    verbose_name_plural = 'productos estimados'


class ProjectEstimationMaterialsInLine(admin.TabularInline):
    """
    Tabular inline for the Materials shown in the Project Estimation
    admin page.
    """
    model = models.ProjectEstimationMaterialsEntry

    verbose_name = 'material'
    verbose_name_plural = 'materiales estimados'


class ProjectEstimationAdmin(VersionAdmin):
    """
    Specifies the details for the admin app in regard
    to the ProjectEstimation entity.
    """
    inlines = [
        ProjectEstimationProductsInLine,
        ProjectEstimationMaterialsInLine,
    ]
    readonly_fields = ('author',)

    def save_model(self, request, obj, form, change):
        """
        Overrides the default save function for the ProjectEstimation model. After each ProjectEstimation is saved,
        the author field is filled with the current user.
        """
        obj.author = request.user
        obj.save()


admin_site.register(models.Repair)
admin_site.register(models.Project, ProjectAdmin)
admin_site.register(models.ProjectEstimation, ProjectEstimationAdmin)
admin_site.register(models.ProjectVisit)
admin_site.register(models.SalesVisit)
