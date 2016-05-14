from __future__ import unicode_literals

import utils
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('inventories', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(utils.migrations.load_products_inventory)
    ]
