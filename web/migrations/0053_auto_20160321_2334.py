# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0052_auto_20151224_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photos',
            name='description',
            field=models.TextField(null=True, verbose_name='Description', blank=True),
        ),
    ]
