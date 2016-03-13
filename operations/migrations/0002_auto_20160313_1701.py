# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-13 23:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='end_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='fecha de finalización'),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='fecha de inicio'),
        ),
    ]