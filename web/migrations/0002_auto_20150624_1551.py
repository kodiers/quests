# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questsusers',
            options={'verbose_name': 'Quest user', 'verbose_name_plural': 'Quests users'},
        ),
    ]
