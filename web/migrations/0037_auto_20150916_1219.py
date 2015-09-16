# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0036_auto_20150909_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventswinners',
            name='player',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='eventswinners',
            name='team',
            field=models.ForeignKey(null=True, blank=True, to='web.Teams'),
        ),
    ]
