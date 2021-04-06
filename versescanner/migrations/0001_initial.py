# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 09:15
import elisio.Syllable
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=45)),
                ('short_name', models.CharField(max_length=18)),
                ('abbreviation', models.CharField(max_length=10)),
                ('birth_year', models.IntegerField()),
                ('dying_year', models.IntegerField()),
                ('floruit_start', models.IntegerField()),
                ('floruit_end', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DatabaseVerse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('alternative', models.CharField(max_length=1)),
                ('contents', models.CharField(max_length=70)),
                ('saved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DeviantSyllable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', enumfields.fields.EnumField(enum=elisio.Syllable.Weight, max_length=10)),
                ('contents', models.CharField(max_length=8)),
                ('sequence', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DeviantWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stem', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Opus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=40)),
                ('abbreviation', models.CharField(max_length=10)),
                ('alternative_name', models.CharField(max_length=40)),
                ('publication', models.IntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elisio.Author')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elisio.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('start_year', models.IntegerField()),
                ('end_year', models.IntegerField()),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Poem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('nickname', models.CharField(max_length=20)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elisio.Book')),
            ],
        ),
        migrations.CreateModel(
            name='WordOccurrence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=20)),
                ('struct', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='deviantsyllable',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elisio.DeviantWord'),
        ),
        migrations.AddField(
            model_name='databaseverse',
            name='poem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elisio.Poem'),
        ),
        migrations.AddField(
            model_name='book',
            name='opus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elisio.Opus'),
        ),
        migrations.AddField(
            model_name='author',
            name='period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elisio.Period'),
        ),
        migrations.AddField(
            model_name='wordoccurrence',
            name='verse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elisio.DatabaseVerse'),
        ),
    ]