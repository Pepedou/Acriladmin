from django.contrib.auth.models import User
from django.core.validators import EmailValidator, URLValidator
from django.db import models
from utils.validators import phone_regex_validator, zip_code_regex_validator


class Address(models.Model):
    """
    A simple geographical address.
    """

    interior_number = models.CharField(verbose_name='No. int.', max_length=10, blank=True)
    exterior_number = models.CharField(verbose_name='No. ext.', max_length=10)
    street = models.CharField(verbose_name='Calle', max_length=45)
    town = models.CharField(verbose_name='Delegación/Municipio', max_length=45, blank=True)
    city = models.CharField(verbose_name='Ciudad', max_length=45, blank=True)
    state = models.CharField(verbose_name='Estado', max_length=45, blank=True)
    country = models.CharField(verbose_name='País', max_length=45, blank=True)
    zip_code = models.CharField(verbose_name='CP', max_length=5, blank=True, validators=[zip_code_regex_validator])

    class Meta:
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'

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

    name = models.CharField(verbose_name='Nombre(s)', max_length=20)
    paternal_last_name = models.CharField(verbose_name='Apellido paterno', max_length=20)
    maternal_last_name = models.CharField(verbose_name='Apellido materno', max_length=20)
    gender = models.PositiveSmallIntegerField(verbose_name='Género', choices=GENDER_CHOICES)
    phone = models.CharField(verbose_name='Tel.', max_length=14, blank=True, validators=[phone_regex_validator])
    email = models.EmailField(verbose_name='Correo electrónico', blank=True,
                              validators=[EmailValidator(message='Correo electrónico inválido.')])
    picture = models.ImageField(verbose_name='Imagen de perfil', blank=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name='Dirección', null=True, blank=True)

    class Meta:
        verbose_name = 'Perfil individual'
        verbose_name = 'Perfiles individuales'

    def __str__(self):
        return self.full_name


class EmployeeRole(models.Model):
    """
    Describes a role assigned to an employee.
    """
    name = models.CharField(verbose_name='Nombre del rol', max_length=20)
    description = models.CharField(verbose_name='Descripción del rol', max_length=50)

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name


class Employee(models.Model):
    """
    An employee that works for Acrilfrasa.
    """
    number = models.CharField(verbose_name='Número', max_length=45, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario', null=True, blank=True)
    seniority = models.DateField(verbose_name='Antigüedad')
    is_active = models.BooleanField(verbose_name='Activo', default=True)
    role = models.ForeignKey(EmployeeRole, on_delete=models.PROTECT, verbose_name='Rol')
    profile = models.OneToOneField(PersonProfile, verbose_name='Datos del empleado', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return str(self.profile)


class OrganizationProfile(models.Model):
    """
    Stores information about an organization or company.
    """
    name = models.CharField(verbose_name='Name', max_length=45)
    contact = models.ForeignKey(PersonProfile, on_delete=models.SET_NULL, verbose_name='Persona de contacto', null=True,
                                blank=True)
    phone = models.CharField(verbose_name='Tel.', max_length=14, blank=True, validators=[phone_regex_validator])
    website = models.URLField(verbose_name='Sitio web', max_length=45, blank=True,
                              validators=[URLValidator(message="URL inválida.")])
    email = models.EmailField(verbose_name='Correo electrónico', blank=True,
                              validators=[EmailValidator(message="Correo electrónico inválido.")])
    picture = models.ImageField(verbose_name='Imagen', blank=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name='Dirección', null=True, blank=True)

    class Meta:
        verbose_name = 'Perfil de la organización'
        verbose_name_plural = 'Perfiles de las organizaciones'

    def __str__(self):
        return self.name


class Client(models.Model):
    """
    One of Acrilfrasa's clients.
    """
    profile = models.OneToOneField(OrganizationProfile, verbose_name='Datos del cliente', on_delete=models.PROTECT)
    client_since = models.DateField(verbose_name='Antigüedad', auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return str(self.profile)


class BranchOffice(models.Model):
    """
    A location involved in the business activities of the firm.
    """
    profile = models.OneToOneField(OrganizationProfile, verbose_name='Datos de la sucursal', on_delete=models.CASCADE)
    administrator = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Administrador de la sucursal',
                                      related_name="administrated_branches")
    employees = models.ManyToManyField(Employee, verbose_name='Empleados de la sucursal', blank=True)

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'

    def __str__(self):
        return str(self.profile)
