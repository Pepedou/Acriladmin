from back_office.models import Client, Employee
from django.db import models
from inventories.models import ProductDefinition, Material, DurableGoodDefinition, MaterialDefinition


class Service(models.Model):
    """
    A service provided by Acrilfrasa to a customer.
    """
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Repair(models.Model):
    """
    A repair made on a durable good.
    """
    durable_good = models.ForeignKey(DurableGoodDefinition, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField(max_length=300)
    requested_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='requested_repairs')
    authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='authorized_repairs')

    def __str__(self):
        return str(self.durable_good)


class Project(models.Model):
    """
    A project developed for a client by Acrilfrasa.
    """
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=100, blank=True)
    supervisor = models.ForeignKey(Employee, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProjectEstimation(models.Model):
    """
    An estimation made by an employee of the materials and cost
    for a project.
    """
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.project)


class ProjectEstimationProductsEntry(models.Model):
    """
    The quantity of a specific product needed for a
    project.
    """
    product = models.ForeignKey(ProductDefinition, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=0)
    project_estimation = models.ForeignKey(ProjectEstimation, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}: {1}".format(self.product.name, self.quantity)


class ProjectEstimationMaterialsEntry(models.Model):
    """
    The quantity of a specific material needed for a
    project.
    """
    material = models.ForeignKey(MaterialDefinition, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=0)
    project_estimation = models.ForeignKey(ProjectEstimation, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}: {1}".format(self.material.name, self.quantity)
