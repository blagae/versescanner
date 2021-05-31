# Generated by Django 3.1.7 on 2021-04-01 20:28

from django.db import migrations, models

import versescanner.util.utils


class Migration(migrations.Migration):

    dependencies = [
        ('versescanner', '0008_auto_20171003_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batchrun',
            name='commit',
            field=models.CharField(default=versescanner.util.utils.get_commit, max_length=80),
        ),
        migrations.AlterField(
            model_name='batchrun',
            name='initiator',
            field=models.CharField(default='', max_length=80),
        ),
    ]
