import operations.models as models
from django.contrib import admin
from operations.forms.project_products_inline_forms import ProjectProductsInLineForm


class ProjectProductsInLine(admin.TabularInline):
    model = models.ProjectProductsEntry
    form = ProjectProductsInLineForm


class ProjectMaterialsInLine(admin.TabularInline):
    model = models.ProjectMaterialsEntry


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Datos administrativos", {
            'fields': ('name', 'description', 'supervisor', 'client', 'sales_agent',
                       'start_date', 'end_date')
        }),
        ("Datos operativos", {
            'fields': ('vehicle', 'has_been_paid', 'cost',)
        }),
    )
    inlines = [
        ProjectProductsInLine,
        ProjectMaterialsInLine
    ]

class ProjectEstimationProductsInLine(admin.TabularInline):
    model = models.ProjectEstimationProductsEntry


class ProjectEstimationMaterialsInLine(admin.TabularInline):
    model = models.ProjectEstimationMaterialsEntry


class ProjectEstimationAdmin(admin.ModelAdmin):
    inlines = [
        ProjectEstimationProductsInLine,
        ProjectEstimationMaterialsInLine,
    ]


admin.site.register(models.Service)
admin.site.register(models.Repair)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.ProjectEstimation, ProjectEstimationAdmin)
admin.site.register(models.ProjectVisit)
admin.site.register(models.SalesVisit)
