# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20150625_1720'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskstatistics',
            options={'verbose_name_plural': 'Tasks statistics', 'ordering': ('time',), 'verbose_name': 'Task statistic'},
        ),
    ]
