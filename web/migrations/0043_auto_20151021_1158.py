# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0042_auto_20151021_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pages',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]
