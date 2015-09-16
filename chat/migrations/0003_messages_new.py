# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_contactlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='new',
            field=models.BooleanField(verbose_name='New message', default=True),
        ),
    ]
