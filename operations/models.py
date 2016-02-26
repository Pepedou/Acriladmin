from django.db import models

# Create your models here.
# class Repair(models.Model):
#     """
#     A repair on a durable good.
#     """
#     durable_good = models.ForeignKey(DurableGoodDefinition, on_delete=models.CASCADE)
#     date = models.DateField()
#     reason = models.TextField(max_length=300)
#     requested_by = models.ForeignKey(Employee, on_delete=models.PROTECT)
#     authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT)