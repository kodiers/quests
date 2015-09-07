# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0029_taskstatistics_started'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskstatistics',
            name='time',
            field=models.CharField(blank=True, max_length=64, verbose_name='Executed time', null=True),
        ),
    ]
