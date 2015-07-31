# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0017_auto_20150731_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='registered_players',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Registered users', blank=True, related_name='regitered_players'),
        ),
        migrations.AlterField(
            model_name='events',
            name='registered_teams',
            field=models.ManyToManyField(verbose_name='Registered teams', blank=True, to='web.Teams'),
        ),
    ]
