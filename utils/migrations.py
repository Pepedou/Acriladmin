import csv
import os
from decimal import Decimal
from distutils.util import grok_environment_error

from django.conf import settings

from inventories.models import Product


def load_employee_groups(apps, schema_editor):
    """
    Loads the employee_groups.csv into the database.
    """
    new_employee_groups = []
    employee_group_class = apps.get_model("auth", "Group")

    del schema_editor

    with open(os.path.join(settings.BASE_DIR, "var/csv/employee_groups.csv")) as file:
        content = csv.DictReader(file, delimiter='|')

        for row in content:
            employee_group = employee_group_class(name=row['name'])
            new_employee_groups.append(employee_group)

    employee_group_class.objects.bulk_create(new_employee_groups)


def load_permissions(apps, schema_editor):
    """
    Assigns auth permissions to each group.
    """
    permission_class = apps.get_model("auth", "Permission")
    employee_group_class = apps.get_model("auth", "Group")

    del schema_editor

    print(str(permission_class.objects.all()))

    for group in employee_group_class.objects.all():
        perms = []

        if group.name == 'Ventas':
            perms = permission_class.objects.filter(codename__in=[
                'add_sale',
                'change_sale',
                'add_invoice',
                'change_invoice',

            ])
        elif group.name == 'Jefe de almacén':
            perms = permission_class.objects.filter(codename__in=[
                'add_product',
                'change_product',
                'delete_product',
                'add_producttransfer',
                'change_producttransfer',
                'add_productreimbursement',
                'change_productreimbursement'
            ])
        print("Permisos para {0}: {1}".format(str(group.name), ", ".join([str(x) for x in perms])))
        group.permissions = perms


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
    branch_office_class = apps.get_model("back_office", "BranchOffice")

    default_branch_office = branch_office_class.objects.first()

    del schema_editor

    with open(os.path.join(settings.BASE_DIR, "var/csv/employees.csv")) as file:
        content = csv.DictReader(file, delimiter=',')

        for row in content:
            employee = employee_class(username=row['username'],
                                      first_name=row['first_name'],
                                      last_name=row['last_name'],
                                      email=row['email'],
                                      branch_office=default_branch_office)
            new_employees.append(employee)

    employee_class.objects.bulk_create(new_employees)


def load_products_inventory(apps, schema_editor):
    """
    Loads the product_inventory.csv file into the database.
    """
    new_products = []
    product_class = apps.get_model("inventories", "Product")

    del schema_editor

    with open(os.path.join(settings.BASE_DIR, "var/csv/product_inventory.csv")) as file:
        content = csv.DictReader(file, delimiter='|')

        for row in content:
            new_product = product_class(sku=row['CLAVE'].strip(),
                                        description=row['DESCRIPCION'].strip(),
                                        search_description=row['DESCRIPCION_BUSQUEDA'].strip(),
                                        line=_get_index_for_product_line(row['LINEA'].strip()),
                                        engraving=row['GRABADO'].strip(),
                                        color=row['COLOR'].strip(),
                                        length=Decimal(row['LONGITUD']),
                                        thickness=Decimal(row['ANCHO']),
                                        width=Decimal(row['ESPESOR']),
                                        is_composite=False)

            new_products.append(new_product)

    product_class.objects.bulk_create(new_products)


def _get_index_for_product_line(product_line):
    """
    Returns the integer that corresponds to a Product Line.
    :param product_line: The line for which the index is needed.
    :return: The line's index.
    """
    if product_line == "ACR":
        return Product.ACR
    elif product_line == "ACRILETA":
        return Product.ACRILETA
    elif product_line == "ACRIMP":
        return Product.ACRIMP
    elif product_line == "ACRIP":
        return Product.ACRIP
    elif product_line == "ADE":
        return Product.ADE
    elif product_line == "DIFUSOR":
        return Product.DIFUSOR
    elif product_line == "DOM":
        return Product.DOM
    elif product_line == "GLASLINER":
        return Product.GLASLINER
    elif product_line == "LAM":
        return Product.LAM
    elif product_line == "OTROS":
        return Product.OTROS
    elif product_line == "PERFIL":
        return Product.PERFIL
    elif product_line == "PLA":
        return Product.PLA
    elif product_line == "POL":
        return Product.POL
    elif product_line == "POL SOL":
        return Product.POL_SOL
    elif product_line == "SILI":
        return Product.SILI
    elif product_line == "STON":
        return Product.STON
    else:
        raise NotImplementedError(product_line)


def load_product_prices(apps, schema_editor):
    """
    Loads the product prices' from the product_inventory.csv file into
    the database.
    """
    product_prices = []
    product_price_class = apps.get_model("finances", "ProductPrice")
    product_class = apps.get_model("inventories", "Product")
    employee_class = apps.get_model("back_office", "Employee")

    author = employee_class.objects.filter(username='lfragoso').first()

    del schema_editor

    with open(os.path.join(settings.BASE_DIR, "var/csv/product_inventory.csv")) as file:
        content = csv.DictReader(file, delimiter='|')

        for row in content:
            product = product_class.objects.filter(sku=row['CLAVE'].strip()).first()
            new_product_price = product_price_class(product=product,
                                                    price=Decimal(row['PRECIO']),
                                                    authorized_by_id=author.id)

            product_prices.append(new_product_price)

    product_price_class.objects.bulk_create(product_prices)


def load_employee_groups_relationships(apps, schema_editor):
    """
    Loads the employee-group relationships from the employee_groups_relationship.csv
    file into the database.
    """
    employee_group_class = apps.get_model("auth", "Group")
    employee_class = apps.get_model("back_office", "Employee")

    del schema_editor

    with open(os.path.join(settings.BASE_DIR,
                           "var/csv/employee_groups_relationship.csv")) as file:
        content = csv.DictReader(file, delimiter='|')

        for row in content:
            group = employee_group_class.objects.filter(name=row['group']).first()
            employees_usernames = row['employees_usernames'].split(',')
            employees = employee_class.objects.filter(username__in=employees_usernames)

            for employee in employees:
                employee.groups.add(group)
                employee.save()
