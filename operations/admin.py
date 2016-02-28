from django.contrib import admin
import operations.models as models

admin.site.register(models.Service)
admin.site.register(models.Repair)
admin.site.register(models.Project)
admin.site.register(models.ProjectEstimation)
