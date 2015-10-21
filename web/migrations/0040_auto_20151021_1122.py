# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0039_faq'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'verbose_name_plural': 'F.A.Q.', 'verbose_name': 'F.A.Q.', 'ordering': ('created',)},
        ),
        migrations.AddField(
            model_name='faq',
            name='created',
            field=models.DateField(default=datetime.datetime(2015, 10, 21, 11, 22, 22, 788686, tzinfo=utc), auto_now=True, verbose_name='Created'),
            preserve_default=False,
        ),
    ]
