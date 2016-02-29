# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-28 23:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventories', '0005_auto_20160228_2320'),
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectestimation',
            old_name='economic_cost',
            new_name='cost',
        ),
        migrations.AlterField(
            model_name='projectestimation',
            name='materials',
            field=models.ManyToManyField(to='inventories.MaterialDefinition'),
        ),
        migrations.RemoveField(
            model_name='projectestimation',
            name='products',
        ),
        migrations.AddField(
            model_name='projectestimation',
            name='products',
            field=models.ManyToManyField(to='inventories.ProductDefinition'),
        ),
        migrations.AlterField(
            model_name='projectestimation',
            name='project',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='operations.Project'),
        ),
    ]
