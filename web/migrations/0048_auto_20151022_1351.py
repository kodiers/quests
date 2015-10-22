# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0047_auto_20151022_1345'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FAQ',
        ),
        migrations.DeleteModel(
            name='Pages',
        ),
    ]
