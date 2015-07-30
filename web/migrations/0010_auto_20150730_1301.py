# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0009_auto_20150728_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='teams',
            name='creator',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='teams',
            name='players',
            field=models.ManyToManyField(related_name='team_players', to=settings.AUTH_USER_MODEL),
        ),
    ]
