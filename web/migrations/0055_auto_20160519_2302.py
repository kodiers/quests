# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0054_auto_20160519_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='place',
            field=models.ForeignKey(null=True, verbose_name='Place', blank=True, to='web.EventsPlaces'),
        ),
    ]
