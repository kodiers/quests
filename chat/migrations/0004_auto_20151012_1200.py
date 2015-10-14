# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_messages_new'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactlist',
            name='contacts',
        ),
        migrations.RemoveField(
            model_name='contactlist',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='messages',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='messages',
            name='to_user',
        ),
        migrations.DeleteModel(
            name='ContactList',
        ),
        migrations.DeleteModel(
            name='Messages',
        ),
    ]
