import csv

import os
from django.conf import settings


def load_employee_roles(apps, schema_editor):
    """
    Loads the employee_roles.csv into the database.
    """
    new_employee_roles = []
    employee_role_class = apps.get_model("back_office", "EmployeeRole")

    del schema_editor

    with open(os.path.join(settings.BASE_DIR, "var/csv/employee_roles.csv")) as file:
        content = csv.DictReader(file, delimiter='|')

        for row in content:
            employee_role = employee_role_class(name=row['name'], description=row['description'])
            new_employee_roles.append(employee_role)

    employee_role_class.objects.bulk_create(new_employee_roles)


def load_branch_offices(apps, schema_editor):
    """
    Loads the branch_offices.csv into the database.
    """
    new_branch_offices = []
    branch_offices_class = apps.get_model("back_office", "BranchOffice")

    del schema_editor

    with open(os.path.join(settings.BASE_DIR, "var/csv/branch_offices.csv")) as file:
        content = csv.DictReader(file, delimiter=',')

        for row in content:
            branch_office = branch_offices_class(name=row['name'])
            new_branch_offices.append(branch_office)

    branch_offices_class.objects.bulk_create(new_branch_offices)


def load_employees(apps, schema_editor):
    """
    Loads the employees.csv into the database.
    """
    new_employees = []
    employee_class = apps.get_model("back_office", "Employee")

    del schema_editor

    with open(os.path.join(settings.BASE_DIR, "var/csv/employees.csv")) as file:
        content = csv.DictReader(file, delimiter=',')

        for row in content:
            employee = employee_class(username=row['username'],
                                      first_name=row['first_name'],
                                      last_name=row['last_name'],
                                      email=row['email'])
            new_employees.append(employee)

    employee_class.objects.bulk_create(new_employees)


def load_products_inventory(apps, schema_editor):
    """
    Loads the product_inventory.csv file into the database.
    """
    new_products = []
    product_definition_class = apps.get_model("inventories", "Product")

    del schema_editor

    with open(os.path.join(settings.BASE_DIR, "var/csv/product_inventory.csv")) as file:
        content = csv.DictReader(file, delimiter=',')
        width = 0
        length = 0
        thickness = 0

        for row in content:
            for string in row['descripcion'].split():
                if '*' in string:
                    try:
                        width = float(string.split('*')[0])
                        length = float(string.split('*')[1])
                    except ValueError:
                        continue
                elif 'MM' in string:
                    try:
                        thickness = float(string.split('M')[0])
                    except ValueError:
                        continue

            new_product = product_definition_class(sku=row['clave'],
                                                   description=row['descripcion'],
                                                   width=width,
                                                   length=length,
                                                   thickness=thickness,
                                                   is_composite=False)
            new_products.append(new_product)

        product_definition_class.objects.bulk_create(new_products)
