from django.contrib import admin
import finances.models as models

admin.site.register(models.Order)
admin.site.register(models.OrderProducts)
admin.site.register(models.OrderServices)
admin.site.register(models.Invoice)
admin.site.register(models.ProductInvoice)
admin.site.register(models.ProductPrice)
admin.site.register(models.MaterialCost)
admin.site.register(models.ServiceInvoice)
admin.site.register(models.Transaction)
