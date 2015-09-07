# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0030_auto_20150907_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskstatistics',
            name='time',
            field=models.IntegerField(null=True, verbose_name='Executed time', blank=True),
        ),
    ]
