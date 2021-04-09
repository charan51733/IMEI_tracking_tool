# Generated by Django 3.1.7 on 2021-04-08 18:10

import device.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='oem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('oem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.oem')),
            ],
            options={
                'unique_together': {('oem', 'name')},
            },
        ),
        migrations.CreateModel(
            name='device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imei', models.IntegerField(unique=True, validators=[device.models.validate_imei], verbose_name='IMEI')),
                ('wfi_mac', models.CharField(blank=True, max_length=225, null=True, verbose_name='WFI MAC')),
                ('iccid', models.CharField(blank=True, max_length=225, null=True, verbose_name='ICCID')),
                ('imsi', models.CharField(blank=True, max_length=225, null=True, verbose_name='IMSI')),
                ('mdn', models.CharField(blank=True, max_length=225, null=True, verbose_name='MDN')),
                ('assignee', models.CharField(blank=True, default=None, max_length=225, null=True, verbose_name='ASSIGNEE')),
                ('assigned_date', models.CharField(blank=True, default='04/08/2021', max_length=50, null=True, validators=[device.models.dateValidate], verbose_name='ASSIGNED DATE')),
                ('purpose', models.CharField(blank=True, max_length=225, null=True, verbose_name='PURPOSE')),
                ('return_date', models.CharField(blank=True, max_length=50, null=True, validators=[device.models.dateValidate], verbose_name='RETURN DATE')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='COMMENT')),
                ('delivery', models.CharField(choices=[('Early Dev Samples', 'Early Dev Samples'), ('Pre-LE', 'Pre-LE'), ('LE', 'LE'), ('FAI', 'FAI'), ('FFW', 'FFW'), ('VIP KIT', 'VIP KIT')], default=('Early Dev Samples', 'Early Dev Samples'), max_length=225, verbose_name='DELIVERY')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.model', verbose_name='MODEL')),
                ('oem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.oem', verbose_name='OEM')),
            ],
        ),
    ]
