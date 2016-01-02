# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('cinema_id', models.TextField(serialize=False, primary_key=True)),
                ('cinema_name', models.CharField(max_length=40)),
                ('district', models.CharField(max_length=20)),
                ('road', models.CharField(max_length=20)),
                ('busstation', models.CharField(max_length=20, db_column='busStation')),
                ('phone', models.CharField(max_length=50)),
                ('businesshoursbegin', models.TimeField(db_column='businessHoursBegin')),
                ('businesshoursend', models.TimeField(db_column='businessHoursEnd')),
                ('estimate', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'cinema',
                'managed': False,
            },
        ),
    ]
