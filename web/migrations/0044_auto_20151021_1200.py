# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0043_auto_20151021_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pages',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
