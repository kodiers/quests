# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0028_auto_20150828_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskstatistics',
            name='started',
            field=models.BooleanField(default=False, verbose_name='Task started'),
        ),
    ]
