# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0026_todayevents'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskstatistics',
            name='completed',
            field=models.BooleanField(verbose_name='Is task completed for user or team', default=False),
        ),
    ]
