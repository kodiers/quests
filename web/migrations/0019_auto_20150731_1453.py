# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0018_auto_20150731_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventstatistics',
            name='event',
            field=models.OneToOneField(to='web.Events', verbose_name='Event'),
        ),
        migrations.AlterField(
            model_name='eventstatistics',
            name='player',
            field=models.OneToOneField(verbose_name='Player', to=settings.AUTH_USER_MODEL, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='eventstatistics',
            name='team',
            field=models.OneToOneField(verbose_name='Team', to='web.Teams', blank=True, null=True),
        ),
    ]
