# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-18 23:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('inventories', '0004_producttransfer_rejection_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producttransfer',
            name='rejection_reason',
            field=models.TextField(blank=True, max_length=250, verbose_name='motivo de rechazo'),
        ),
    ]