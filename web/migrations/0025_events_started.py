# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0024_auto_20150819_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='started',
            field=models.BooleanField(default=False, verbose_name='Started'),
        ),
    ]
