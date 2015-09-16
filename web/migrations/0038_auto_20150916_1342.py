# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0037_auto_20150916_1219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='messages',
            name='to_user',
        ),
        migrations.DeleteModel(
            name='Messages',
        ),
    ]
