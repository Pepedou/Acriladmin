# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-13 23:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('back_office', '0003_auto_20160313_1744'),
        ('operations', '0003_projectvisit'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesVisit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', geoposition.fields.GeopositionField(max_length=42, verbose_name='localización')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='back_office.Address', verbose_name='dirección')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='back_office.Client', verbose_name='cliente')),
                ('sales_agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_office.Employee', verbose_name='agente de ventas')),
            ],
            options={
                'verbose_name_plural': 'visitas de ventas',
                'verbose_name': 'visita de ventas',
            },
        ),
    ]