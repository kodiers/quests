# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0004_auto_20151012_1200'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('have_new_message', models.BooleanField(default=False, verbose_name='New message')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Users')),
            ],
            options={
                'verbose_name_plural': 'Chats',
                'verbose_name': 'Chat',
            },
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('text', models.TextField(verbose_name='Message')),
                ('new', models.BooleanField(default=False, verbose_name='New')),
                ('datetime', models.DateTimeField(verbose_name='Date and time', auto_now=True)),
                ('chat', models.ForeignKey(to='chat.Chat', verbose_name='Chat')),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
            ],
            options={
                'verbose_name_plural': 'Messages',
                'verbose_name': 'Message',
            },
        ),
    ]
