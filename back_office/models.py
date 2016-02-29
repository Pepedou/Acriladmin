from django.contrib.auth.models import User
from django.db import models


class Address(models.Model):
    """
    A simple geographical address.
    """
    interior_number = models.CharField(max_length=10, blank=True)
    exterior_number = models.CharField(max_length=10, blank=True)
    street = models.CharField(max_length=45, blank=True)
    town = models.CharField(max_length=45, blank=True)
    city = models.CharField(max_length=45, blank=True)
    state = models.CharField(max_length=45, blank=True)
    country = models.CharField(max_length=45, blank=True)
    zip_code = models.PositiveSmallIntegerField(blank=True)

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

    name = models.CharField(max_length=20)
    paternal_last_name = models.CharField(max_length=20)
    maternal_last_name = models.CharField(max_length=20)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES)
    phone = models.CharField(max_length=14, blank=True)
    email = models.EmailField(blank=True)
    picture = models.ImageField(blank=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.full_name


class EmployeeRole(models.Model):
    """
    Describes a role assigned to an employee.
    """
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Employee(models.Model):
    """
    An employee that works for Acrilfrasa.
    """
    number = models.CharField(max_length=45, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    seniority = models.DateField()
    is_active = models.BooleanField(default=True)
    role = models.ForeignKey(EmployeeRole, on_delete=models.PROTECT)
    profile = models.OneToOneField(PersonProfile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.profile)


class OrganizationProfile(models.Model):
    """
    Stores information about an organization or company.
    """
    name = models.CharField(max_length=45)
    contact = models.ForeignKey(PersonProfile, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=14, blank=True)
    website = models.URLField(max_length=45, blank=True)
    email = models.EmailField(blank=True)
    picture = models.ImageField(blank=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    """
    One of Acrilfrasa's clients.
    """
    profile = models.OneToOneField(OrganizationProfile, on_delete=models.PROTECT)
    client_since = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.profile)


class BranchOffice(models.Model):
    """
    A location involved in the business activities of the firm.
    """
    profile = models.OneToOneField(OrganizationProfile, on_delete=models.CASCADE)
    administrator = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="administrated_branches")
    employees = models.ManyToManyField(Employee, blank=True)

    def __str__(self):
        return str(self.profile)
