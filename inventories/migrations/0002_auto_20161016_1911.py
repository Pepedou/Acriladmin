# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-17 00:11
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('inventories', '0001_initial'),
        ('back_office', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finances', '0002_auto_20161016_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttransfer',
            name='sale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='finances.Sale', verbose_name='venta cancelada relacionada'),
        ),
        migrations.AddField(
            model_name='producttransfer',
            name='source_branch',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='product_transfers_as_source_branch', to='back_office.BranchOffice',
                                    verbose_name='sucursal de origen'),
        ),
        migrations.AddField(
            model_name='producttransfer',
            name='target_branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='product_transfers_as_target_branch', to='back_office.BranchOffice',
                                    verbose_name='sucursal de destino'),
        ),
        migrations.AddField(
            model_name='productsinventory',
            name='branch',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='back_office.BranchOffice',
                                       verbose_name='sucursal'),
        ),
        migrations.AddField(
            model_name='productsinventory',
            name='last_updater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL,
                                    verbose_name='autor de la última actualización'),
        ),
        migrations.AddField(
            model_name='productsinventory',
            name='supervisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                    related_name='products_inventories_supervised', to=settings.AUTH_USER_MODEL,
                                    verbose_name='supervisor'),
        ),
        migrations.AddField(
            model_name='productremoval',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventories.ProductsInventory',
                                    verbose_name='inventario'),
        ),
        migrations.AddField(
            model_name='productremoval',
            name='product_transfer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    to='inventories.ProductTransfer', verbose_name='transferencia de producto'),
        ),
        migrations.AddField(
            model_name='productremoval',
            name='provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    to='back_office.Provider', verbose_name='proveedor'),
        ),
        migrations.AddField(
            model_name='productremoval',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL,
                                    verbose_name='usuario'),
        ),
        migrations.AddField(
            model_name='productreimbursement',
            name='inventory',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT,
                                    to='inventories.ProductsInventory', verbose_name='inventario'),
        ),
        migrations.AddField(
            model_name='productreimbursement',
            name='sale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='finances.Sale', verbose_name='venta relacionada'),
        ),
        migrations.AddField(
            model_name='productinventoryitem',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.ProductsInventory',
                                    verbose_name='inventario'),
        ),
        migrations.AddField(
            model_name='productinventoryitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.Product',
                                    verbose_name='producto'),
        ),
        migrations.AddField(
            model_name='productentry',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventories.ProductsInventory',
                                    verbose_name='inventario'),
        ),
        migrations.AddField(
            model_name='productentry',
            name='purchase_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventories.PurchaseOrder',
                                    verbose_name='orden de compra'),
        ),
        migrations.AddField(
            model_name='productcomponent',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.Material',
                                    verbose_name='material'),
        ),
        migrations.AddField(
            model_name='productcomponent',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.Product',
                                    verbose_name='producto'),
        ),
        migrations.AddField(
            model_name='materialsinventory',
            name='branch',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='back_office.BranchOffice',
                                       verbose_name='sucursal'),
        ),
        migrations.AddField(
            model_name='materialsinventory',
            name='last_updater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL,
                                    verbose_name='autor de la última actualización'),
        ),
        migrations.AddField(
            model_name='materialsinventory',
            name='supervisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                    related_name='materials_inventories_supervised', to=settings.AUTH_USER_MODEL,
                                    verbose_name='supervisor'),
        ),
        migrations.AddField(
            model_name='materialinventoryitem',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.MaterialsInventory',
                                    verbose_name='inventario'),
        ),
        migrations.AddField(
            model_name='materialinventoryitem',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.Material',
                                    verbose_name='material'),
        ),
        migrations.AddField(
            model_name='enteredproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventories.Product',
                                    verbose_name='producto'),
        ),
        migrations.AddField(
            model_name='enteredproduct',
            name='product_entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.ProductEntry',
                                    verbose_name='ingreso'),
        ),
        migrations.AddField(
            model_name='durablegoodsinventory',
            name='branch',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='back_office.BranchOffice',
                                       verbose_name='sucursal'),
        ),
        migrations.AddField(
            model_name='durablegoodsinventory',
            name='last_updater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL,
                                    verbose_name='autor de la última actualización'),
        ),
        migrations.AddField(
            model_name='durablegoodsinventory',
            name='supervisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                    related_name='durable_goods_inventories_supervised', to=settings.AUTH_USER_MODEL,
                                    verbose_name='supervisor'),
        ),
        migrations.AddField(
            model_name='durablegoodinventoryitem',
            name='durable_good',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.DurableGood',
                                    verbose_name='activo'),
        ),
        migrations.AddField(
            model_name='durablegoodinventoryitem',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.DurableGoodsInventory',
                                    verbose_name='inventario'),
        ),
        migrations.AddField(
            model_name='consumablesinventory',
            name='branch',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='back_office.BranchOffice',
                                       verbose_name='sucursal'),
        ),
        migrations.AddField(
            model_name='consumablesinventory',
            name='last_updater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL,
                                    verbose_name='autor de la última actualización'),
        ),
        migrations.AddField(
            model_name='consumablesinventory',
            name='supervisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                    related_name='consumables_inventories_supervised', to=settings.AUTH_USER_MODEL,
                                    verbose_name='supervisor'),
        ),
        migrations.AddField(
            model_name='consumableinventoryitem',
            name='consumable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.Consumable',
                                    verbose_name='consumible'),
        ),
        migrations.AddField(
            model_name='consumableinventoryitem',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.ConsumablesInventory',
                                    verbose_name='inventario'),
        ),
    ]
