# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0022_tasks_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='time',
            field=models.CharField(max_length=64, blank=True, null=True, verbose_name='Time for task'),
        ),
    ]
