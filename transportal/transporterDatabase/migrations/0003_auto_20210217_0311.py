# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-02-17 03:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transporterDatabase', '0002_auto_20210217_0302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitrointeraction',
            name='stimConcentration',
            field=models.FloatField(null=True),
        ),
    ]
