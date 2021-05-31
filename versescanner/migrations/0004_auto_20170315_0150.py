# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-15 00:50
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('versescanner', '0003_auto_20160518_2114'),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timing', models.DateTimeField(auto_now=True)),
                ('initiator', models.CharField(max_length=40)),
                ('commit', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='BatchRunResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('failure', models.CharField(blank=True, max_length=70)),
                ('structure', models.CharField(max_length=8)),
                ('zeleny', models.CharField(max_length=17)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='versescanner.BatchRun')),
            ],
        ),
        migrations.AddField(
            model_name='batchrunresult',
            name='verse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='versescanner.Verse'),
        ),
    ]
