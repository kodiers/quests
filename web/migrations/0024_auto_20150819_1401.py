# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0023_auto_20150812_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='answer',
            field=models.TextField(null=True, blank=True, verbose_name='Answer'),
        ),
    ]
