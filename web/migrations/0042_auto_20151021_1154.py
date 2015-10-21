# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0041_pages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pages',
            name='content',
            field=models.TextField(),
        ),
    ]
