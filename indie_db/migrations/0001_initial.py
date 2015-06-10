# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('deathdate', models.DateField(blank=True, null=True)),
                ('group', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('alternate_name', models.CharField(max_length=200)),
                ('role', models.CharField(max_length=200)),
                ('contributing_artist', models.ForeignKey(blank=True, null=True, to='indie_db.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='ProductionCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Production Companies',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('link', models.CharField(max_length=400)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('kind', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('extra_data', models.TextField(blank=True, null=True)),
                ('created', models.DateField()),
                ('city', models.CharField(max_length=200)),
                ('self_published', models.BooleanField(default=False)),
                ('styles', models.CharField(max_length=200)),
                ('contributors', models.ManyToManyField(to='indie_db.Contributor')),
                ('creator', models.ForeignKey(to='indie_db.Artist')),
                ('link', models.ForeignKey(to='indie_db.URL')),
                ('production_company', models.ForeignKey(blank=True, null=True, to='indie_db.ProductionCompany')),
            ],
            options={
                'verbose_name_plural': 'Works of Art',
                'verbose_name': 'Work of Art',
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='productioncompany',
            name='link',
            field=models.ForeignKey(to='indie_db.URL'),
        ),
        migrations.AddField(
            model_name='artist',
            name='link',
            field=models.ForeignKey(to='indie_db.URL'),
        ),
        migrations.AddField(
            model_name='artist',
            name='members',
            field=models.ManyToManyField(to='indie_db.Artist', blank=True, null=True, related_name='members_rel_+'),
        ),
    ]
