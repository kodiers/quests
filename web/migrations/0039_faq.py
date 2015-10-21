# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0038_auto_20150916_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('question', models.TextField(verbose_name='Question')),
                ('answer', models.TextField(verbose_name='Answer')),
            ],
            options={
                'verbose_name': 'F.A.Q.',
                'verbose_name_plural': 'F.A.Q.',
            },
        ),
    ]
