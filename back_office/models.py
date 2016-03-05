from django.contrib.auth.models import User
from django.core.validators import EmailValidator, URLValidator
from django.db import models
from utils.validators import phone_regex_validator, zip_code_regex_validator


class Address(models.Model):
    """
    A simple geographical address.
    """

    interior_number = models.CharField(verbose_name='número interior', max_length=10, blank=True)
    exterior_number = models.CharField(verbose_name='número exterior', max_length=10)
    street = models.CharField(verbose_name='calle', max_length=45)
    town = models.CharField(verbose_name='municipio', max_length=45, blank=True)
    city = models.CharField(verbose_name='ciudad', max_length=45, blank=True)
    state = models.CharField(verbose_name='estado', max_length=45, blank=True)
    country = models.CharField(verbose_name='país', max_length=45, blank=True)
    zip_code = models.CharField(verbose_name='CP', max_length=5, blank=True, validators=[zip_code_regex_validator])

    class Meta:
        verbose_name = 'dirección'
        verbose_name_plural = 'direcciones'

    def __str__(self):
        return "{0}, {1}, {2}".format(self.exterior_number, self.street, self.town)


class PersonProfile(models.Model):
    """Stores personal information about a person."""
    MALE = 0
    FEMALE = 1
    GENDER_CHOICES = (
        (MALE, "Masculino"),
        (FEMALE, "Femenino")
    )

    @property
    def full_name(self):
        return "{0} {1} {2}".format(self.name, self.paternal_last_name, self.maternal_last_name).rstrip()

    name = models.CharField(verbose_name='nombre(s)', max_length=20)
    paternal_last_name = models.CharField(verbose_name='apellido paterno', max_length=20)
    maternal_last_name = models.CharField(verbose_name='apellido materno', max_length=20)
    gender = models.PositiveSmallIntegerField(verbose_name='género', choices=GENDER_CHOICES)
    phone = models.CharField(verbose_name='teléfono', max_length=14, blank=True, validators=[phone_regex_validator])
    email = models.EmailField(verbose_name='correo electrónico', blank=True,
                              validators=[EmailValidator(message='Correo electrónico inválido.')])
    picture = models.ImageField(verbose_name='imagen de perfil', blank=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name='dirección', null=True, blank=True)

    class Meta:
        verbose_name = 'perfil individual'
        verbose_name_plural = 'perfiles individuales'

    def __str__(self):
        return self.full_name


class EmployeeRole(models.Model):
    """
    Describes a role assigned to an employee.
    """
    ADMINISTRATOR = 0
    TELEPHONE_SALES = 1
    FIELD_SALES = 2
    INSTALLER = 3
    DRIVER = 4
    DOME_PRODUCER = 5
    WAREHOUSE_CHIEF = 6
    NAME_CHOICES = (
        (ADMINISTRATOR, "Administrador"),
        (TELEPHONE_SALES, "Ventas telefónicas"),
        (FIELD_SALES, "Ventas en campo"),
        (INSTALLER, "Instalador"),
        (DRIVER, "Chofer"),
        (DOME_PRODUCER, "Productor de domos"),
        (WAREHOUSE_CHIEF, "Jefe de almacén"),
    )

    name = models.CharField(verbose_name='nombre del rol', max_length=20, primary_key=True)
    description = models.CharField(verbose_name='descripción del rol', max_length=50)

    class Meta:
        verbose_name = 'rol'
        verbose_name_plural = 'roles'

    def __str__(self):
        return self.name


class Employee(models.Model):
    """
    An employee that works for Acrilfrasa.
    """
    number = models.CharField(verbose_name='número', max_length=45, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='usuario', null=True, blank=True)
    seniority = models.DateField(verbose_name='antigüedad')
    is_active = models.BooleanField(verbose_name='activo', default=True)
    role = models.ForeignKey(EmployeeRole, on_delete=models.PROTECT, verbose_name='rol', limit_choices_to={''})
    profile = models.OneToOneField(PersonProfile, verbose_name='datos del empleado', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'empleado'
        verbose_name_plural = 'empleados'

    def __str__(self):
        return str(self.profile)


class OrganizationProfile(models.Model):
    """
    Stores information about an organization or company.
    """
    name = models.CharField(verbose_name='name', max_length=45)
    contact = models.ForeignKey(PersonProfile, on_delete=models.SET_NULL, verbose_name='persona de contacto', null=True,
                                blank=True)
    phone = models.CharField(verbose_name='teléfono', max_length=14, blank=True, validators=[phone_regex_validator])
    website = models.URLField(verbose_name='sitio web', max_length=45, blank=True,
                              validators=[URLValidator(message="URL inválida.")])
    email = models.EmailField(verbose_name='correo electrónico', blank=True,
                              validators=[EmailValidator(message="Correo electrónico inválido.")])
    picture = models.ImageField(verbose_name='imagen', blank=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name='dirección', null=True, blank=True)

    class Meta:
        verbose_name = 'perfil de la organización'
        verbose_name_plural = 'perfiles de las organizaciones'

    def __str__(self):
        return self.name


class Client(models.Model):
    """
    One of Acrilfrasa's clients.
    """
    profile = models.OneToOneField(OrganizationProfile, verbose_name='datos del cliente', on_delete=models.PROTECT)
    client_since = models.DateField(verbose_name='antigüedad', auto_now_add=True)

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    def __str__(self):
        return str(self.profile)


class BranchOffice(models.Model):
    """
    A location involved in the business activities of the firm.
    """
    profile = models.OneToOneField(OrganizationProfile, verbose_name='datos de la sucursal', on_delete=models.CASCADE)
    administrator = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='administrador de la sucursal',
                                      related_name="administrated_branches")
    employees = models.ManyToManyField(Employee, verbose_name='empleados de la sucursal', blank=True)

    class Meta:
        verbose_name = 'sucursal'
        verbose_name_plural = 'sucursales'

    def __str__(self):
        return str(self.profile)
