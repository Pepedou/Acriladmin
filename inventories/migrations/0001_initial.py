# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-27 03:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('back_office', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, verbose_name='nombre')),
                ('description', models.CharField(blank=True, max_length=50, verbose_name='descripción')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='imagen')),
                ('brand', models.CharField(max_length=45, verbose_name='marca')),
                ('model', models.CharField(max_length=45, verbose_name='modelo')),
                ('prefix', models.SmallIntegerField(choices=[(0, 'N/A'), (-24, 'y'), (-21, 'z'), (-18, 'a'), (-15, 'f'), (-12, 'p'), (-9, 'n'), (-6, 'μ'), (-3, 'm'), (-2, 'c'), (-1, 'd'), (1, 'da'), (2, 'h'), (3, 'k'), (6, 'M'), (9, 'G'), (12, 'T'), (15, 'P'), (18, 'E'), (21, 'Z'), (24, 'Y')], default=0, verbose_name='prefijo de unidad')),
                ('unit', models.PositiveSmallIntegerField(choices=[(0, 'N/A'), (1, 'm'), (2, 'in'), (3, 'ft'), (4, 'yd'), (5, 'mi'), (6, 'g'), (7, 's'), (8, 'pz'), (9, 'l')], default=0, verbose_name='unidad')),
            ],
            options={
                'verbose_name_plural': 'consumibles',
                'verbose_name': 'consumible',
            },
        ),
        migrations.CreateModel(
            name='ConsumableInventoryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='cantidad')),
                ('consumable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.Consumable', verbose_name='consumible')),
            ],
            options={
                'verbose_name_plural': 'elementos de inventario de consumibles',
                'verbose_name': 'elemento de inventario de consumibles',
            },
        ),
        migrations.CreateModel(
            name='ConsumablesInventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, verbose_name='nombre')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='última actualización')),
                ('branch', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='back_office.BranchOffice', verbose_name='sucursal')),
                ('last_updater', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='autor de la última actualización')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='consumables_inventories_supervised', to=settings.AUTH_USER_MODEL, verbose_name='supervisor')),
            ],
            options={
                'verbose_name_plural': 'inventarios de consumibles',
                'verbose_name': 'inventario de consumibles',
            },
        ),
        migrations.CreateModel(
            name='DurableGood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, verbose_name='nombre')),
                ('description', models.CharField(max_length=50, verbose_name='descripción')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='imagen')),
                ('brand', models.CharField(max_length=45, verbose_name='marca')),
                ('model', models.CharField(max_length=45, verbose_name='modelo')),
                ('prefix', models.SmallIntegerField(choices=[(0, 'N/A'), (-24, 'y'), (-21, 'z'), (-18, 'a'), (-15, 'f'), (-12, 'p'), (-9, 'n'), (-6, 'μ'), (-3, 'm'), (-2, 'c'), (-1, 'd'), (1, 'da'), (2, 'h'), (3, 'k'), (6, 'M'), (9, 'G'), (12, 'T'), (15, 'P'), (18, 'E'), (21, 'Z'), (24, 'Y')], default=0, verbose_name='prefijo de la unidad')),
                ('unit', models.PositiveSmallIntegerField(choices=[(0, 'N/A'), (1, 'm'), (2, 'in'), (3, 'ft'), (4, 'yd'), (5, 'mi'), (6, 'g'), (7, 's'), (8, 'pz'), (9, 'l')], default=0, verbose_name='unidad')),
            ],
            options={
                'verbose_name_plural': 'activos',
                'verbose_name': 'activo',
            },
        ),
        migrations.CreateModel(
            name='DurableGoodInventoryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='cantidad')),
                ('durable_good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.DurableGood', verbose_name='activo')),
            ],
            options={
                'verbose_name_plural': 'elementos de inventarios de activos',
                'verbose_name': 'elemento de inventario de activos',
            },
        ),
        migrations.CreateModel(
            name='DurableGoodsInventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, verbose_name='nombre')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='última actualización')),
                ('branch', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='back_office.BranchOffice', verbose_name='sucursal')),
                ('last_updater', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='autor de la última actualización')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='durable_goods_inventories_supervised', to=settings.AUTH_USER_MODEL, verbose_name='supervisor')),
            ],
            options={
                'verbose_name_plural': 'inventarios de activos',
                'verbose_name': 'inventario de activos',
            },
        ),
        migrations.CreateModel(
            name='ExchangedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='cantidad')),
            ],
            options={
                'verbose_name_plural': 'productos intercambiados (salen)',
                'verbose_name': 'producto intercambiado (sale)',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, verbose_name='nombre')),
                ('description', models.CharField(max_length=50, verbose_name='descripción')),
                ('image', models.FileField(blank=True, upload_to='', verbose_name='imagen')),
                ('color', models.CharField(default='color', max_length=10)),
                ('length', models.DecimalField(decimal_places=2, default=0.01, max_digits=6, verbose_name='longitud')),
                ('width', models.DecimalField(decimal_places=2, default=0.01, max_digits=6, verbose_name='anchura')),
                ('thickness', models.DecimalField(decimal_places=2, default=0.01, max_digits=6, verbose_name='grosor')),
                ('weight', models.DecimalField(decimal_places=2, default=0.01, max_digits=6, verbose_name='peso')),
                ('prefix', models.SmallIntegerField(blank=True, choices=[(0, 'N/A'), (-24, 'y'), (-21, 'z'), (-18, 'a'), (-15, 'f'), (-12, 'p'), (-9, 'n'), (-6, 'μ'), (-3, 'm'), (-2, 'c'), (-1, 'd'), (1, 'da'), (2, 'h'), (3, 'k'), (6, 'M'), (9, 'G'), (12, 'T'), (15, 'P'), (18, 'E'), (21, 'Z'), (24, 'Y')], default=0, verbose_name='prefijo de unidad')),
                ('unit', models.PositiveSmallIntegerField(choices=[(0, 'N/A'), (1, 'm'), (2, 'in'), (3, 'ft'), (4, 'yd'), (5, 'mi'), (6, 'g'), (7, 's'), (8, 'pz'), (9, 'l')], default=0, verbose_name='unidad')),
            ],
            options={
                'verbose_name_plural': 'materiales',
                'verbose_name': 'material',
            },
        ),
        migrations.CreateModel(
            name='MaterialInventoryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='cantidad')),
            ],
            options={
                'verbose_name_plural': 'elementos de inventario de materiales',
                'verbose_name': 'elemento de inventario de materiales',
            },
        ),
        migrations.CreateModel(
            name='MaterialsInventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, verbose_name='nombre')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='última actualización')),
                ('branch', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='back_office.BranchOffice', verbose_name='sucursal')),
                ('last_updater', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='autor de la última actualización')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='materials_inventories_supervised', to=settings.AUTH_USER_MODEL, verbose_name='supervisor')),
            ],
            options={
                'verbose_name_plural': 'inventarios de materiales',
                'verbose_name': 'inventario de materiales',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=45, unique=True, verbose_name='SKU')),
                ('description', models.CharField(max_length=100, verbose_name='descripción')),
                ('line', models.PositiveSmallIntegerField(choices=[(0, 'Acrílico'), (1, 'Policarbonato'), (2, 'Celular'), (3, 'Plástico'), (4, 'Lámina'), (5, 'Rejillas'), (6, 'Domos'), (7, 'Silicones'), (8, 'Otra')], default=8, verbose_name='línea')),
                ('engraving', models.CharField(blank=True, max_length=45, verbose_name='grabado')),
                ('color', models.CharField(blank=True, max_length=10, verbose_name='color')),
                ('length', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='longitud (m)')),
                ('width', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='anchura (m)')),
                ('thickness', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='espesor (mm)')),
                ('is_composite', models.BooleanField(default=False, verbose_name='es compuesto')),
            ],
            options={
                'verbose_name_plural': 'productos',
                'verbose_name': 'producto',
            },
        ),
        migrations.CreateModel(
            name='ProductComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, verbose_name='nombre')),
                ('required_units', models.PositiveSmallIntegerField(default=1, verbose_name='unidades requeridas del componente')),
                ('required_amount_per_unit', models.DecimalField(decimal_places=2, default=1.0, max_digits=5, verbose_name='cantidad requerida por unidad')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.Material', verbose_name='material')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.Product', verbose_name='producto')),
            ],
            options={
                'verbose_name_plural': 'componentes de productos',
                'verbose_name': 'componente de un producto',
            },
        ),
        migrations.CreateModel(
            name='ProductInventoryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='cantidad')),
            ],
            options={
                'verbose_name_plural': 'elementos de inventario de productos',
                'verbose_name': 'elemento de inventario de productos',
            },
        ),
        migrations.CreateModel(
            name='ProductReimbursement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monetary_difference', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='diferencia')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='fecha de devolución')),
                ('from_branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_reimbursement_as_from_branch', to='back_office.BranchOffice', verbose_name='intercambia con')),
                ('to_branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_reimbursement_as_to_branch', to='back_office.BranchOffice', verbose_name='devuelve a')),
            ],
            options={
                'verbose_name_plural': 'devoluciones de productos',
                'verbose_name': 'devolución de productos',
            },
        ),
        migrations.CreateModel(
            name='ProductsInventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, verbose_name='nombre')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='última actualización')),
                ('branch', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='back_office.BranchOffice', verbose_name='sucursal')),
                ('last_updater', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='autor de la última actualización')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products_inventories_supervised', to=settings.AUTH_USER_MODEL, verbose_name='supervisor')),
            ],
            options={
                'verbose_name_plural': 'inventarios de productos',
                'verbose_name': 'inventario de productos',
            },
        ),
        migrations.CreateModel(
            name='ProductTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='cantidad')),
                ('is_confirmed', models.BooleanField(default=False, verbose_name='confirmada')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.Product', verbose_name='producto')),
                ('source_branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_transfers_as_source_branch', to='back_office.BranchOffice', verbose_name='sucursal de origen')),
                ('target_branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_transfers_as_target_branch', to='back_office.BranchOffice', verbose_name='sucursal de destino')),
            ],
            options={
                'verbose_name_plural': 'transferencias de producto',
                'verbose_name': 'transferencia de producto',
            },
        ),
        migrations.CreateModel(
            name='ReturnedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='cantidad')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.Product', verbose_name='producto')),
                ('reimbursement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.ProductReimbursement', verbose_name='devolución')),
            ],
            options={
                'verbose_name_plural': 'productos devueltos (entran)',
                'verbose_name': 'producto devuelto (entra)',
            },
        ),
        migrations.AddField(
            model_name='productinventoryitem',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.ProductsInventory', verbose_name='inventario'),
        ),
        migrations.AddField(
            model_name='productinventoryitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.Product', verbose_name='producto'),
        ),
        migrations.AddField(
            model_name='materialinventoryitem',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.MaterialsInventory', verbose_name='inventario'),
        ),
        migrations.AddField(
            model_name='materialinventoryitem',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.Material', verbose_name='material'),
        ),
        migrations.AddField(
            model_name='exchangedproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.Product', verbose_name='producto'),
        ),
        migrations.AddField(
            model_name='exchangedproduct',
            name='reimbursement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.ProductReimbursement', verbose_name='devolución'),
        ),
        migrations.AddField(
            model_name='durablegoodinventoryitem',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.DurableGoodsInventory', verbose_name='inventario'),
        ),
        migrations.AddField(
            model_name='consumableinventoryitem',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.ConsumablesInventory', verbose_name='inventario'),
        ),
    ]
