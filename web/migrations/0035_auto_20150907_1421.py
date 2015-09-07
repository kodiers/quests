# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0034_eventswinners'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventstatistics',
            name='end_time',
            field=models.DateTimeField(blank=True, verbose_name='End time', null=True),
        ),
        migrations.AddField(
            model_name='eventstatistics',
            name='start_time',
            field=models.DateTimeField(blank=True, verbose_name='Start time', null=True),
        ),
    ]
