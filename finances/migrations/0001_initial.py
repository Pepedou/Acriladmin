# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-01 03:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventories', '0001_initial'),
        ('back_office', '0001_initial'),
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('authorized_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='back_office.Employee')),
                ('material', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inventories.Material')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Solicitada'), (1, 'En progreso'), (2, 'Completa'), (3, 'Cancelada'), (4, 'Devuelta')])),
                ('target', models.PositiveSmallIntegerField(choices=[(0, 'Productos'), (1, 'Servicios'), (2, 'Productos y servicios')])),
                ('date', models.DateField()),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('shipping_and_handling', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='back_office.Client')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventories.Product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderServices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.Order')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operations.Service')),
            ],
        ),
        migrations.CreateModel(
            name='ProductInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.Invoice')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventories.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('authorized_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='back_office.Employee')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inventories.Product')),
            ],
        ),
        migrations.CreateModel(
            name='RepairCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('repair', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='operations.Repair')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.Invoice')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operations.Service')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='finances.Invoice')),
                ('payed_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='back_office.Client')),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.Order'),
        ),
    ]
