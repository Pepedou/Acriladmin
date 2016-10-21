# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-21 04:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventories', '0003_auto_20161019_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producttransfer',
            name='confirmed_quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='cantidad confirmada'),
        ),
        migrations.AlterField(
            model_name='producttransfer',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='cantidad'),
        ),
    ]
