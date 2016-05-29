from cities_light.abstract_models import (AbstractCity, AbstractRegion,
                                          AbstractCountry)
from cities_light.receivers import connect_default_signals
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import EmailValidator, URLValidator
from django.db import models
from django.db.models import Q
from utils.validators import phone_regex_validator, zip_code_regex_validator


class Country(AbstractCountry):
    """
    Default implementation of abstract class AbstractCountry
    of the django-cities-light app.
    """

    class Meta:
        verbose_name = 'país'
        verbose_name_plural = 'paises'


class Region(AbstractRegion):
    """
    Default implementation of abstract class AbstractRegion
    of the django-cities-light app.
    """

    class Meta:
        verbose_name = 'región'
        verbose_name_plural = 'regiones'


class City(AbstractCity):
    """
    Default implementation of abstract class AbstractCity
    of the django-cities-light app.
    """

    class Meta:
        verbose_name = 'ciudad'
        verbose_name_plural = 'ciudades'


connect_default_signals(Country)
connect_default_signals(Region)
connect_default_signals(City)


class Address(models.Model):
    """
    A simple geographical address.
    """

    interior_number = models.CharField(verbose_name='número interior', max_length=10, blank=True)
    exterior_number = models.CharField(verbose_name='número exterior', max_length=10)
    street = models.CharField(verbose_name='calle', max_length=45)
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='ciudad', related_name='acriladmin_city',
                             max_length=45, blank=True)
    state = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='estado', related_name='acriladmin_state',
                              max_length=45, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='país',
                                related_name='acriladmin_country', max_length=45, blank=True)
    zip_code = models.CharField(verbose_name='CP', max_length=5, blank=True, validators=[zip_code_regex_validator])

    class Meta:
        verbose_name = 'dirección'
        verbose_name_plural = 'direcciones'

    def __str__(self):
        return "{0}, {1}, {2}".format(self.exterior_number, self.street, self.state)


class EmployeeRole(models.Model):
    """
    Describes a role assigned to an employee.
    """
    ADMINISTRATOR = "Administrador"
    TELEPHONE_SALES = "Ventas telefónicas"
    FIELD_SALES = "Ventas en campo"
    SALES_AGENT = "Agente de ventas"
    INSTALLER = "Instalador"
    DRIVER = "Chofer"
    DOME_PRODUCER = "Productor de domos"
    WAREHOUSE_CHIEF = "Jefe de almacén"
    NAME_CHOICES = (
        (ADMINISTRATOR, ADMINISTRATOR),
        (TELEPHONE_SALES, TELEPHONE_SALES),
        (FIELD_SALES, FIELD_SALES),
        (SALES_AGENT, SALES_AGENT),
        (INSTALLER, INSTALLER),
        (DRIVER, DRIVER),
        (DOME_PRODUCER, DOME_PRODUCER),
        (WAREHOUSE_CHIEF, WAREHOUSE_CHIEF),
    )

    name = models.CharField(verbose_name='nombre del rol', max_length=20, primary_key=True)
    description = models.CharField(verbose_name='descripción del rol', max_length=50)

    class Meta:
        verbose_name = 'rol'
        verbose_name_plural = 'roles'

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    """
    An employee that works for Acrilfrasa.
    """
    MALE = 0
    FEMALE = 1
    GENDER_CHOICES = (
        (MALE, "Masculino"),
        (FEMALE, "Femenino")
    )

    gender = models.PositiveSmallIntegerField(default=MALE, verbose_name='género', choices=GENDER_CHOICES)
    phone = models.CharField(verbose_name='teléfono', max_length=15, blank=True, validators=[phone_regex_validator])
    picture = models.ImageField(verbose_name='imagen de perfil', blank=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name='dirección', null=True, blank=True)
    roles = models.ManyToManyField(EmployeeRole, verbose_name='roles')

    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    class Meta:
        verbose_name = 'empleado'
        verbose_name_plural = 'empleados'

    def __str__(self):
        return self.get_full_name()


class Client(models.Model):
    """
    One of Acrilfrasa's clients.
    """

    name = models.CharField(verbose_name='nombre', max_length=45)
    phone = models.CharField(verbose_name='teléfono', max_length=15, blank=True, validators=[phone_regex_validator])
    website = models.URLField(verbose_name='sitio web', max_length=45, blank=True,
                              validators=[URLValidator(message="URL inválida.")])
    email = models.EmailField(verbose_name='correo electrónico', blank=True,
                              validators=[EmailValidator(message="Correo electrónico inválido.")])
    picture = models.ImageField(verbose_name='imagen', blank=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name='dirección', null=True, blank=True)
    client_since = models.DateField(verbose_name='antigüedad', auto_now_add=True)

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    def __str__(self):
        return self.name


class BranchOffice(models.Model):
    """
    A location involved in the business activities of the firm.
    """
    name = models.CharField(verbose_name='nombre de la sucursal', max_length=45)
    administrator = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True,
                                      verbose_name='administrador de la sucursal',
                                      related_name="administrated_branches",
                                      limit_choices_to=Q(roles__name=EmployeeRole.ADMINISTRATOR) & ~Q(username='root'))
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name='dirección', null=True, blank=True)
    phone = models.CharField(verbose_name='teléfono', max_length=15, blank=True, validators=[phone_regex_validator])
    email = models.EmailField(verbose_name='correo electrónico', blank=True,
                              validators=[EmailValidator(message="Correo electrónico inválido.")])
    website = models.URLField(verbose_name='sitio web', max_length=45, blank=True,
                              validators=[URLValidator(message="URL inválida.")])
    employees = models.ManyToManyField(Employee, verbose_name='empleados de la sucursal', blank=True,
                                       limit_choices_to=~Q(username='root'))

    class Meta:
        verbose_name = 'sucursal'
        verbose_name_plural = 'sucursales'

    def __str__(self):
        return self.name
