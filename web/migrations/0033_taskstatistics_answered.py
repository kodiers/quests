# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0032_eventstatistics_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskstatistics',
            name='answered',
            field=models.BooleanField(verbose_name='Task is correctly answered', default=False),
        ),
    ]
