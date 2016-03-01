import csv

import os
from django.conf import settings


def load_employee_roles(apps, schema_editor):
    new_employee_roles = []
    employee_role_class = apps.get_model("back_office", "EmployeeRole")

    del schema_editor

    with open(os.path.join(settings.BASE_DIR, "var/csv/employee_roles.csv")) as file:
        content = csv.DictReader(file, delimiter='|')

        for row in content:
            employee_role = employee_role_class(name=row['name'], description=row['description'])
            new_employee_roles.append(employee_role)

    employee_role_class.objects.bulk_create(new_employee_roles)