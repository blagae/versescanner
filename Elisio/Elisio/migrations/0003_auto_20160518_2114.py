# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 09:37
from django.db import migrations


def load_initial_data(self, orm):
    from Elisio.filemanager import sync_db
    sync_db()


class Migration(migrations.Migration):
    dependencies = [
        ('Elisio', '0001_initial'),
        ('Elisio', '0002_auto_20160501_1137'),
    ]

    operations = [
        migrations.RunPython(load_initial_data)
    ]
