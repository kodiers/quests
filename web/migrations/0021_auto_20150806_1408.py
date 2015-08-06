# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0020_auto_20150731_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='phone',
            field=models.CharField(null=True, blank=True, verbose_name='Phone number', max_length=128),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='site',
            field=models.CharField(null=True, blank=True, verbose_name='Web site', max_length=128),
        ),
    ]
