# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('indie_db', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('authorname', models.CharField(unique=True, max_length=200)),
                ('tagline', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('website', models.CharField(max_length=400)),
                ('user', models.OneToOneField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('body_en', models.TextField()),
                ('body_fr', models.TextField()),
                ('publish', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('artist_link', models.ForeignKey(blank=True, null=True, to='indie_db.Artist')),
                ('author', models.ForeignKey(to='blog.Author')),
            ],
            options={
                'verbose_name_plural': 'Blog Entries',
                'verbose_name': 'Blog Entry',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag'),
        ),
        migrations.AddField(
            model_name='entry',
            name='work_link',
            field=models.ForeignKey(blank=True, null=True, to='indie_db.Work'),
        ),
    ]
