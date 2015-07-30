# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_auto_20150730_1302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teams',
            name='creator',
        ),
    ]
