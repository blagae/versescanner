# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-09 20:19
import django.db.models.deletion
import enumfields.fields
from django.conf import settings
from django.db import migrations, models

import Elisio.engine.verse.VerseType
import Elisio.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Elisio', '0004_auto_20170315_0150'),
    ]

    operations = [
        migrations.AddField(
            model_name='scansession',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)
        ),
        migrations.AlterField(
            model_name='scansession',
            name='commit',
            field=models.CharField(default=Elisio.utils.get_commit, max_length=40),
        ),
        migrations.AlterField(
            model_name='scansession',
            name='initiator',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='scanverseresult',
            name='scanned_as',
            field=enumfields.fields.EnumField(default=1, enum=Elisio.engine.verse.VerseType.VerseType, max_length=10),
            preserve_default=False,
        ),
    ]
