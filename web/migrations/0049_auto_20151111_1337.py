# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0048_auto_20151022_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='min_players',
            field=models.IntegerField(verbose_name='Minimum players', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='max_players',
            field=models.IntegerField(verbose_name='Maximum players', blank=True, null=True),
        ),
    ]
