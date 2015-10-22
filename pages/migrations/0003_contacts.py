# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20151022_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('url', models.SlugField(verbose_name='URL', unique=True)),
                ('phone', models.CharField(max_length=128, verbose_name='Phone')),
                ('address', models.TextField(null=True, verbose_name='Address', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('map', models.TextField(null=True, verbose_name='Map script', blank=True)),
                ('comments', tinymce.models.HTMLField(null=True, verbose_name='Comments', blank=True)),
            ],
            options={
                'verbose_name': 'Contacts',
                'verbose_name_plural': 'Contacts',
            },
        ),
    ]
