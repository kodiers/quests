# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0025_events_started'),
    ]

    operations = [
        migrations.CreateModel(
            name='TodayEvents',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('event', models.OneToOneField(to='web.Events')),
            ],
        ),
    ]
