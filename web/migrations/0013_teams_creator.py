# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0012_remove_teams_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='teams',
            name='creator',
            field=models.OneToOneField(blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Creator'),
        ),
    ]
