# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0021_auto_20150806_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='time',
            field=models.DurationField(verbose_name='Time for task', blank=True, null=True),
        ),
    ]
