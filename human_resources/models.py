from django.contrib.auth.models import User
from django.db import models


class Address(models.Model):
    """A simple geographical address."""
    interior_number = models.CharField(max_length=5, blank=True)
    exterior_number = models.CharField(max_length=5, blank=True)
    street = models.CharField(max_length=20, blank=True)
    town = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)
    zip_code = models.PositiveSmallIntegerField(blank=True)


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
    gender = models.IntegerField(choices=GENDER_CHOICES)
    phone = models.CharField(max_length=14, blank=True)
    email = models.EmailField(blank=True)
    picture = models.ImageField()
    address = models.ForeignKey(Address, on_delete=models.PROTECT)


class EmployeeRole(models.Model):
    """Describes a role assigned to an employee."""
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)


class Employee(models.Model):
    """An employee that works for the company."""
    number = models.CharField(max_length=45, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    seniority = models.DateField()
    is_active = models.BooleanField(default=True)
    role = models.ForeignKey(EmployeeRole, on_delete=models.PROTECT)
    profile = models.ForeignKey(PersonProfile, on_delete=models.PROTECT)


class Client(models.Model):
    """One of Acrilfrasa's clients."""
    name = models.CharField(max_length=45)
    contact_profile = models.ForeignKey(PersonProfile, on_delete=models.PROTECT)
