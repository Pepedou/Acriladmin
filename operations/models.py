import django
from back_office.models import Client, Employee, EmployeeRole, Address
from django.db import models
from geoposition.fields import GeopositionField
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
    name = models.CharField(max_length=45, verbose_name='nombre')
    description = models.CharField(max_length=100, blank=True, verbose_name='descripción')
    supervisor = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='projects_supervised',
                                   verbose_name='supervisor')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='cliente')
    sales_agent = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='projects_as_sales_agent',
                                    verbose_name='agente de ventas')
    start_date = models.DateField(default=django.utils.timezone.now, verbose_name='fecha de inicio')
    end_date = models.DateField(default=django.utils.timezone.now, verbose_name='fecha de finalización')
    materials_used = models.ManyToManyField(MaterialDefinition, verbose_name='materiales utilizados')
    products_used = models.ManyToManyField(ProductDefinition, verbose_name='productos utilizados')
    vehicle = models.ForeignKey(DurableGoodDefinition, null=True, blank=True, verbose_name='vehículo utilizado')

    class Meta:
        verbose_name = 'proyecto'
        verbose_name_plural = 'proyectos'

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


class ProjectVisit(models.Model):
    """
    An employee's attendance to a specific project.
    """
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='empleado')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='proyecto')
    notes = models.TextField(blank=True, verbose_name='observaciones')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='fecha y hora')
    position = GeopositionField(verbose_name='localización')

    class Meta:
        verbose_name = 'visita a proyecto'
        verbose_name_plural = 'visitas a proyecto'

    def __str__(self):
        return "{0}: {1} ({2})".format(self.employee, self.project, self.datetime)


class SalesVisit(models.Model):
    """
    A sales agent's visit to an existing or potential client.
    """
    sales_agent = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='agente de ventas',
                                    limit_choices_to={
                                        'roles__name': EmployeeRole.SALES_AGENT
                                    })
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='cliente')
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name='dirección')
    position = GeopositionField(verbose_name='localización')

    class Meta:
        verbose_name = 'visita de ventas'
        verbose_name_plural = 'visitas de ventas'

    def __str__(self):
        return "{0}: {1}".format(self.sales_agent, self.address)
