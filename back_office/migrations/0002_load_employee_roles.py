# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-01 03:03
from __future__ import unicode_literals

import utils.migrations
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('back_office', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(utils.migrations.load_employee_roles)
    ]
