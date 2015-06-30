# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20150630_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='registered_players',
            field=models.ManyToManyField(null=True, related_name='regitered_players', blank=True, verbose_name='Regitered users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='events',
            name='registered_teams',
            field=models.ManyToManyField(null=True, to='web.Teams', blank=True, verbose_name='Registered teams'),
        ),
    ]
