# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0019_auto_20150731_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventstatistics',
            name='event',
            field=models.ForeignKey(verbose_name='Event', to='web.Events'),
        ),
    ]
