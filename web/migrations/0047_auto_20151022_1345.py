# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import tinymce.models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0046_pages'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pages',
            options={'verbose_name': 'Page', 'verbose_name_plural': 'Pages', 'ordering': ('created',)},
        ),
        migrations.AddField(
            model_name='pages',
            name='ceo_description',
            field=models.TextField(blank=True, verbose_name='META description', null=True),
        ),
        migrations.AddField(
            model_name='pages',
            name='ceo_keywords',
            field=models.TextField(blank=True, verbose_name='META keywords', null=True),
        ),
        migrations.AddField(
            model_name='pages',
            name='created',
            field=models.DateField(verbose_name='Created', default=datetime.datetime(2015, 10, 22, 13, 44, 46, 288665, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pages',
            name='title',
            field=models.TextField(verbose_name='Page title', default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pages',
            name='url',
            field=models.SlugField(verbose_name='url', default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pages',
            name='content',
            field=tinymce.models.HTMLField(verbose_name='Page content'),
        ),
    ]
