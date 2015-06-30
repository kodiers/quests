# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20150630_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizers',
            name='tariff',
            field=models.ForeignKey(to='web.Tariffs', null=True, blank=True, verbose_name='Tariff'),
        ),
    ]
