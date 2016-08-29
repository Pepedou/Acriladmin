import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Acriladmin.settings")
django.setup()


def assign_product_price_to_all_products(price):
    """
    Assigns the given price to all the products catalogue.
    :param price: The price to assign.
    """
    from inventories.models import Product
    from finances.models import ProductPrice
    from back_office.models import Employee

    user_luis = Employee.objects.filter(first_name="Luis Daniel").first()
    prices = []

    for product in Product.objects.all():
        product_price = ProductPrice(price=price, product=product,
                                     authorized_by=user_luis)
        prices.append(product_price)

    ProductPrice.objects.bulk_create(prices)


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
        emp.save()


def assign_group_permissions():
    """
    Assigns default permissions for groups.
    """
    from django.contrib.auth.models import Group, Permission

    for group in Group.objects.all():
        perms = []

        if group.name == 'Administrador':
            perms = Permission.objects.all()
        elif group.name == 'Ventas':
            perms = Permission.objects.filter(codename__in=[
                'add_sale',
                'change_sale',
                'add_invoice',
                'change_invoice',
            ])
        elif group.name == 'Jefe de almacén':
            perms = Permission.objects.filter(codename__in=[
                'add_product',
                'change_product',
                'delete_product',
                'add_producttransfer',
                'change_producttransfer',
                'add_productreimbursement',
                'change_productreimbursement'
            ])

        print("Permisos para {0}: {1}".format(str(group.name), ", ".join([x.codename for x in perms])))
        group.permissions = perms


if __name__ == "__main__":
    try:
        print("Executing scripts...")
        fill_up_product_inventories(100)
        set_default_passwords_and_make_staff()
        assign_group_permissions()
        print("Scripts executed successfully!")
    except Exception as ex:
        print("Scripts execution failed!")
        print("{0}".format(ex))
