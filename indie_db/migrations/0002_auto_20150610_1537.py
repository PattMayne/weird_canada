# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indie_db', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='members',
            field=models.ManyToManyField(related_name='members_rel_+', to='indie_db.Artist'),
        ),
    ]
