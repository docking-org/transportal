# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-02-17 03:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transporterDatabase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InVitroSubstrate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concentration', models.CharField(max_length=20, null=True)),
                ('system', models.TextField(null=True)),
                ('ic50', models.CharField(blank=True, max_length=10, null=True)),
                ('km', models.CharField(blank=True, max_length=10, null=True)),
                ('reference', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transporterDatabase.Reference')),
                ('substrate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transporterDatabase.Compound')),
            ],
        ),
        migrations.RenameField(
            model_name='invitrointeraction',
            old_name='stimConc',
            new_name='stimConcentration',
        ),
        migrations.AddField(
            model_name='invitrointeraction',
            name='basalATPaseActivityType',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invitrointeraction',
            name='interactingConcentration',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='invitrointeraction',
            name='km',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='transporter',
            name='species',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='invitrointeraction',
            name='subtype',
            field=models.CharField(blank=True, choices=[('B', 'Basal activity'), ('P', 'Pre-stimulation caused activity')], max_length=1),
        ),
        migrations.AlterField(
            model_name='invitrointeraction',
            name='system',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='invitrosubstrate',
            name='trans',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transporterDatabase.Transporter'),
        ),
    ]
