# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-27 03:05
from __future__ import unicode_literals

import autoslug.fields
import cities_light.abstract_models
from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('gender', models.PositiveSmallIntegerField(choices=[(0, 'Masculino'), (1, 'Femenino')], default=0, verbose_name='género')),
                ('phone', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="El número telefónico debe ingresarse con el formato: '+999999999'. Se permiten hasta 15 dígitos.", regex='^\\+?1?\\d{9,15}$')], verbose_name='teléfono')),
                ('picture', models.ImageField(blank=True, upload_to='', verbose_name='imagen de perfil')),
            ],
            options={
                'verbose_name_plural': 'empleados',
                'verbose_name': 'empleado',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interior_number', models.CharField(blank=True, max_length=10, verbose_name='número interior')),
                ('exterior_number', models.CharField(max_length=10, verbose_name='número exterior')),
                ('street', models.CharField(max_length=45, verbose_name='calle')),
                ('zip_code', models.CharField(blank=True, max_length=5, validators=[django.core.validators.RegexValidator(message='El código postal consta de 5 dígitos.', regex='^[0-9]{5}')], verbose_name='CP')),
            ],
            options={
                'verbose_name_plural': 'direcciones',
                'verbose_name': 'dirección',
            },
        ),
        migrations.CreateModel(
            name='BranchOffice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, verbose_name='nombre de la sucursal')),
                ('phone', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="El número telefónico debe ingresarse con el formato: '+999999999'. Se permiten hasta 15 dígitos.", regex='^\\+?1?\\d{9,15}$')], verbose_name='teléfono')),
                ('email', models.EmailField(blank=True, max_length=254, validators=[django.core.validators.EmailValidator(message='Correo electrónico inválido.')], verbose_name='correo electrónico')),
                ('website', models.URLField(blank=True, max_length=45, validators=[django.core.validators.URLValidator(message='URL inválida.')], verbose_name='sitio web')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='back_office.Address', verbose_name='dirección')),
                ('administrator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='administrated_branches', to=settings.AUTH_USER_MODEL, verbose_name='administrador de la sucursal')),
                ('employees', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='empleados de la sucursal')),
            ],
            options={
                'verbose_name_plural': 'sucursales',
                'verbose_name': 'sucursal',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ascii', models.CharField(blank=True, db_index=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name_ascii')),
                ('geoname_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('alternate_names', models.TextField(blank=True, default='', null=True)),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('display_name', models.CharField(max_length=200)),
                ('search_names', cities_light.abstract_models.ToSearchTextField(blank=True, db_index=True, default='', max_length=4000)),
                ('latitude', models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True)),
                ('population', models.BigIntegerField(blank=True, db_index=True, null=True)),
                ('feature_code', models.CharField(blank=True, db_index=True, max_length=10, null=True)),
            ],
            options={
                'verbose_name_plural': 'ciudades',
                'verbose_name': 'ciudad',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, verbose_name='nombre')),
                ('phone', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="El número telefónico debe ingresarse con el formato: '+999999999'. Se permiten hasta 15 dígitos.", regex='^\\+?1?\\d{9,15}$')], verbose_name='teléfono')),
                ('website', models.URLField(blank=True, max_length=45, validators=[django.core.validators.URLValidator(message='URL inválida.')], verbose_name='sitio web')),
                ('email', models.EmailField(blank=True, max_length=254, validators=[django.core.validators.EmailValidator(message='Correo electrónico inválido.')], verbose_name='correo electrónico')),
                ('picture', models.ImageField(blank=True, upload_to='', verbose_name='imagen')),
                ('client_since', models.DateField(auto_now_add=True, verbose_name='antigüedad')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='back_office.Address', verbose_name='dirección')),
            ],
            options={
                'verbose_name_plural': 'clientes',
                'verbose_name': 'cliente',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ascii', models.CharField(blank=True, db_index=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name_ascii')),
                ('geoname_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('alternate_names', models.TextField(blank=True, default='', null=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('code2', models.CharField(blank=True, max_length=2, null=True, unique=True)),
                ('code3', models.CharField(blank=True, max_length=3, null=True, unique=True)),
                ('continent', models.CharField(choices=[('OC', 'Oceania'), ('EU', 'Europe'), ('AF', 'Africa'), ('NA', 'North America'), ('AN', 'Antarctica'), ('SA', 'South America'), ('AS', 'Asia')], db_index=True, max_length=2)),
                ('tld', models.CharField(blank=True, db_index=True, max_length=5)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'verbose_name_plural': 'paises',
                'verbose_name': 'país',
            },
        ),
        migrations.CreateModel(
            name='EmployeeRole',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='nombre del rol')),
                ('description', models.CharField(max_length=50, verbose_name='descripción del rol')),
            ],
            options={
                'verbose_name_plural': 'roles',
                'verbose_name': 'rol',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ascii', models.CharField(blank=True, db_index=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name_ascii')),
                ('geoname_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('alternate_names', models.TextField(blank=True, default='', null=True)),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('display_name', models.CharField(max_length=200)),
                ('geoname_code', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_office.Country')),
            ],
            options={
                'verbose_name_plural': 'regiones',
                'verbose_name': 'región',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_office.Country'),
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='back_office.Region'),
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(blank=True, max_length=45, on_delete=django.db.models.deletion.CASCADE, related_name='acriladmin_city', to='back_office.City', verbose_name='ciudad'),
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.ForeignKey(blank=True, max_length=45, on_delete=django.db.models.deletion.CASCADE, related_name='acriladmin_country', to='back_office.Country', verbose_name='país'),
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.ForeignKey(blank=True, max_length=45, on_delete=django.db.models.deletion.CASCADE, related_name='acriladmin_state', to='back_office.Region', verbose_name='estado'),
        ),
        migrations.AddField(
            model_name='employee',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='back_office.Address', verbose_name='dirección'),
        ),
        migrations.AddField(
            model_name='employee',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='employee',
            name='roles',
            field=models.ManyToManyField(to='back_office.EmployeeRole', verbose_name='roles'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
