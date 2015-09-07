# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0033_taskstatistics_answered'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventsWinners',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('event', models.OneToOneField(to='web.Events')),
                ('eventstat', models.OneToOneField(to='web.EventStatistics')),
                ('player', models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
                ('team', models.OneToOneField(to='web.Teams', null=True, blank=True)),
            ],
        ),
    ]
