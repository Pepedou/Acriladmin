from django.contrib import admin
import operations.models as models


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
admin.site.register(models.Project)
admin.site.register(models.ProjectEstimation, ProjectEstimationAdmin)
