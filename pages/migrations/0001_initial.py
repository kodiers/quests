# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('question', models.TextField(verbose_name='Question')),
                ('answer', models.TextField(verbose_name='Answer')),
                ('created', models.DateField(verbose_name='Created', auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'F.A.Q.',
                'verbose_name': 'F.A.Q.',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.TextField(verbose_name='Page title')),
                ('content', tinymce.models.HTMLField(verbose_name='Page content')),
                ('url', models.SlugField(verbose_name='url')),
                ('ceo_keywords', models.TextField(blank=True, verbose_name='META keywords', null=True)),
                ('ceo_description', models.TextField(blank=True, verbose_name='META description', null=True)),
                ('created', models.DateField(verbose_name='Created', auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Pages',
                'verbose_name': 'Page',
                'ordering': ('created',),
            },
        ),
    ]
