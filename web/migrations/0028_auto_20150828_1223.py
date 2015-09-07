# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0027_taskstatistics_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskstatistics',
            name='end_time',
            field=models.DateTimeField(null=True, verbose_name='End time', blank=True),
        ),
        migrations.AddField(
            model_name='taskstatistics',
            name='start_time',
            field=models.DateTimeField(null=True, verbose_name='Start time', blank=True),
        ),
    ]
