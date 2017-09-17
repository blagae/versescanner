# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-19 21:47
from __future__ import unicode_literals

import Elisio.engine.VerseFactory
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Elisio', '0005_auto_20170509_2219'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timing', models.DateTimeField(auto_now=True)),
                ('items_at_creation_time', models.IntegerField(null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                           to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='BatchItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='scansession',
            name='user',
        ),
        migrations.AlterField(
            model_name='scansession',
            name='initiator',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='scanverseresult',
            name='structure',
            field=models.CharField(blank=True, max_length=8),
        ),
        migrations.AlterField(
            model_name='scanverseresult',
            name='zeleny',
            field=models.CharField(blank=True, max_length=17),
        ),
        migrations.CreateModel(
            name='DatabaseBatchItem',
            fields=[
                ('batchitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                       parent_link=True, primary_key=True, serialize=False,
                                                       to='Elisio.BatchItem')),
                ('object_type', models.CharField(max_length=10)),
                ('object_id', models.IntegerField(blank=True)),
                ('relation', models.CharField(max_length=10)),
                ('negation', models.BooleanField(default=False)),
            ],
            bases=('Elisio.batchitem',),
        ),
        migrations.CreateModel(
            name='InputBatchItem',
            fields=[
                ('batchitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                       parent_link=True, primary_key=True, serialize=False,
                                                       to='Elisio.BatchItem')),
                ('contents', models.CharField(max_length=70)),
                ('scanned_as', enumfields.fields.EnumField(enum=Elisio.engine.VerseFactory.VerseType, max_length=10,
                                                           null=True)),
            ],
            bases=('Elisio.batchitem',),
        ),
        migrations.AddField(
            model_name='batchitem',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Elisio.Batch'),
        ),
        migrations.AddField(
            model_name='batchitem',
            name='dependent_on',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Elisio.BatchItem'),
        ),
        migrations.AddField(
            model_name='scansession',
            name='batch',
            field=models.ForeignKey(null=True, default=None, on_delete=django.db.models.deletion.CASCADE,
                                    to='Elisio.Batch'),
        ),
        migrations.AddField(
            model_name='scanverseresult',
            name='batch_item',
            field=models.ForeignKey(null=True, default=None, on_delete=django.db.models.deletion.CASCADE,
                                    to='Elisio.BatchItem'),
        ),
    ]
