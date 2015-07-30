# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_auto_20150730_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teams',
            name='creator',
            field=models.ForeignKey(null=True, verbose_name='Creator', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='teams',
            name='players',
            field=models.ManyToManyField(related_name='team_players', to=settings.AUTH_USER_MODEL, verbose_name='Players'),
        ),
    ]
