# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0031_auto_20150907_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventstatistics',
            name='completed',
            field=models.BooleanField(verbose_name='Completed for user/team', default=False),
        ),
    ]
