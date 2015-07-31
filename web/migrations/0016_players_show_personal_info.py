# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0015_auto_20150731_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='players',
            name='show_personal_info',
            field=models.BooleanField(verbose_name='Show personal info', default=False),
        ),
    ]
