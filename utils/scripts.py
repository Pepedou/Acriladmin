import csv
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Acriladmin.settings")
django.setup()

from django.conf import settings
from django.contrib.auth.models import Group, Permission


def fill_up_product_inventories(product_quantity):
    """
    Assigns the quantity given to all product inventories for each product.
    :param product_quantity: The quantity per product to assign.
    """
    from inventories.models import Product, \
        ProductInventoryItem, ProductsInventory
    from back_office.models import BranchOffice, Employee

    user_luis = Employee.objects.filter(first_name="Luis Daniel").first()
    inventory_items = []

    for branch in BranchOffice.objects.all():
        try:
            inventory = branch.productsinventory
        except ProductsInventory.DoesNotExist:
            branch.productsinventory = ProductsInventory(name="Productos de {0}".format(branch.name),
                                                         supervisor=user_luis,
                                                         last_updater=user_luis)
            branch.productsinventory.save()
            inventory = branch.productsinventory

        for product in Product.objects.all():
            inventory_item = ProductInventoryItem(product=product,
                                                  quantity=product_quantity,
                                                  inventory=inventory)
            inventory_items.append(inventory_item)

    ProductInventoryItem.objects.bulk_create(inventory_items)


def set_default_passwords_and_make_staff():
    """
    Sets the default password for all the users. The password
    consists of their first name followed by the first letter of their
    lastname. It also marks them as staff so that they can login.
    """
    from back_office.models import Employee

    for emp in Employee.objects.all():
        emp.is_staff = True
        emp.set_password("{0}{1}".format(
            emp.first_name.split()[0].strip().lower(),
            emp.last_name.split()[0].strip()[0].lower()))

        if emp.username in ['lfragoso', 'cfragoso', 'jfragoso']:
            emp.is_superuser = True

        emp.save()


def load_group_permissions():
    """
    Loads the groups' permissions from the group_permissions.csv
    file into the database.
    """
    with open(os.path.join(settings.BASE_DIR, "var/csv/group_permissions.csv")) as file:
        content = csv.DictReader(file, delimiter='|')

        for row in content:
            group = Group.objects.filter(name=row['group']).first()
            permissions_codenames = row['permissions'].split(',')
            permissions = Permission.objects.filter(codename__in=permissions_codenames)

            group.permissions = permissions
            group.save()


if __name__ == "__main__":
    try:
        print("Executing scripts...")
        fill_up_product_inventories(100)
        set_default_passwords_and_make_staff()
        load_group_permissions()
        print("Scripts executed successfully!")
    except Exception as ex:
        print("Scripts execution failed!")
        print("{0}".format(ex))
