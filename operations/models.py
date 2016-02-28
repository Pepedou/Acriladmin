from back_office.models import Client, Employee
from django.db import models
from inventories.models import ProductDefinition, Material, DurableGoodDefinition


class Service(models.Model):
    """
    A service provided by Acrilfrasa to a customer.
    """
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=100, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class Repair(models.Model):
    """
    A repair made on a durable good.
    """
    durable_good = models.ForeignKey(DurableGoodDefinition, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField(max_length=300)
    requested_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='requested_repairs')
    authorized_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='authorized_repairs')


class Project(models.Model):
    """
    A project developed for a client by Acrilfrasa.
    """
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=100, blank=True)
    supervisor = models.ForeignKey(Employee, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class ProjectEstimation(models.Model):
    """
    An estimation made by an employee of the materials and cost
    for a project.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    economic_cost = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.PositiveIntegerField()
    materials = models.ManyToManyField(Material)
