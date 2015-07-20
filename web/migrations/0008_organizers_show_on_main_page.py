# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_events_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizers',
            name='show_on_main_page',
            field=models.BooleanField(default=False, verbose_name='Best organizer (show on main page)'),
        ),
    ]
