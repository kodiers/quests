# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0035_auto_20150907_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventstatistics',
            name='player',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, verbose_name='Player', null=True),
        ),
        migrations.AlterField(
            model_name='eventstatistics',
            name='team',
            field=models.ForeignKey(to='web.Teams', blank=True, verbose_name='Team', null=True),
        ),
    ]
