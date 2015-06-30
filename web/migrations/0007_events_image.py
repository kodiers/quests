# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20150630_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='image',
            field=models.ImageField(blank=True, null=True, verbose_name='Image', upload_to='images'),
        ),
    ]
