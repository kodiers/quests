# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0053_auto_20160321_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='place',
            field=models.ForeignKey(blank=True, verbose_name='Place', to='web.EventsPlaces', null=True, related_name='event'),
        ),
    ]
