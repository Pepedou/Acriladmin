# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-18 13:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventories', '0001_remove_producttransfer_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producttransfer',
            name='confirmed_quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='cantidad confirmada'),
        ),
    ]
