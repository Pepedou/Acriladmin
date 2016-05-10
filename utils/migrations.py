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


def load_product_inventory(apps, schema_editor):
    """
    Loads the product_inventory.csv into the database.
    """
    new_products = []
    product_definition_class = apps.get_model("inventories", "ProductDefinition")

    del schema_editor

    with open(os.path.join(settings.BASE_DIR, "var/csv/product_inventory.csv")) as file:
        content = csv.DictReader(file, delimiter=',')

        for row in content:
            new_product = product_definition_class(sku=row['clave'],
                                                   name=row['descripcion'],
                                                   short_description=row['descripcion_corta'],
                                                   description=row['descripcion'],
                                                   image="",
                                                   color=row['color'],
                                                   length=0,
                                                   width=0,
                                                   thickness=0,
                                                   weight=0,
                                                   prefix=0,
                                                   unit=0,
                                                   is_composite=False)
            new_products.append(new_product)

        product_definition_class.objects.bulk_create(new_products)
