# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0013_teams_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='event_photos',
            field=models.ManyToManyField(to='web.EventsPhotos', verbose_name='Event photos'),
        ),
        migrations.AlterField(
            model_name='events',
            name='registered_players',
            field=models.ManyToManyField(related_name='regitered_players', to=settings.AUTH_USER_MODEL, verbose_name='Registered users'),
        ),
        migrations.AlterField(
            model_name='events',
            name='registered_teams',
            field=models.ManyToManyField(to='web.Teams', verbose_name='Registered teams'),
        ),
    ]
