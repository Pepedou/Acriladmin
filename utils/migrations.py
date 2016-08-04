import csv
import os
from decimal import Decimal

from django.conf import settings

from inventories.models import Product


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
    product_class = apps.get_model("inventories", "Product")

    del schema_editor

    with open(os.path.join(settings.BASE_DIR, "var/csv/product_inventory.csv")) as file:
        content = csv.DictReader(file, delimiter='|')

        for row in content:
            new_product = product_class(sku=row['CLAVE'].strip(),
                                        description=row['DESCRIPCION'].strip(),
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
    if product_line == "POL":
        return Product.POL
    elif product_line == "POL SOL":
        return Product.POL_SOL
    elif product_line == "LAM":
        return Product.LAM
    elif product_line == "OTROS":
        return Product.OTROS
    elif product_line == "ACR R":
        return Product.ACR_R
    elif product_line == "ACR L":
        return Product.ACR_L
    elif product_line == "ADHESIVO":
        return Product.ADHESIVO
    elif product_line == "ACCESORIO":
        return Product.ACCESORIO
    elif product_line == "DOM":
        return Product.DOM
    elif product_line == "BUR":
        return Product.BUR
    elif product_line == "CORTE":
        return Product.CORTE
    elif product_line == "NINGUNA":
        return Product.NINGUNA
    elif product_line == "ACR-LINEA":
        return Product.ACR_LINEA
    elif product_line == "ACR-GRUESO":
        return Product.ACR_GRUESO
    elif product_line == "ACR-IMPACTO":
        return Product.ACR_IMPACTO
    elif product_line == "GRABADO":
        return Product.GRABADO
    elif product_line == "ACR-ESPEJO":
        return Product.ACR_ESPEJO
    elif product_line == "GALVANIZADA":
        return Product.GALVANIZADA
    elif product_line == "PERFIL":
        return Product.PERFIL
    elif product_line == "NO INCLUIDOS":
        return Product.NO_INCLUIDOS
    elif product_line == "DIFUSOR":
        return Product.DIFUSOR
    elif product_line == "LINER":
        return Product.LINER
    elif product_line == "LAM-LISA":
        return Product.LAM_LISA
    elif product_line == "PLASTICO":
        return Product.PLASTICO
    elif product_line == "REJILLA":
        return Product.REJILLA
    elif product_line == "GLASLINER":
        return Product.GLASLINER
    elif product_line == "SILICON":
        return Product.SILICON
    elif product_line == "POL SOLIDO":
        return Product.POL_SOLIDO
    elif product_line == "SINTRA":
        return Product.SINTRA
    elif product_line == "STONIA":
        return Product.STONIA
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
