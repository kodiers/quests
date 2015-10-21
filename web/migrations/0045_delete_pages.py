# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0044_auto_20151021_1200'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Pages',
        ),
    ]
