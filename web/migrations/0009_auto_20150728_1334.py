# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_organizers_show_on_main_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventsPhotos',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.TextField(null=True, blank=True, verbose_name='Title')),
                ('description', models.TextField(null=True, blank=True, verbose_name='Descrition')),
                ('date', models.DateField(null=True, blank=True, verbose_name='Date')),
                ('image', models.ImageField(upload_to='images')),
            ],
            options={
                'verbose_name_plural': 'Event photos',
                'verbose_name': 'Event photo',
            },
        ),
        migrations.AlterField(
            model_name='events',
            name='registered_players',
            field=models.ManyToManyField(null=True, related_name='regitered_players', blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Registered users'),
        ),
        migrations.AddField(
            model_name='events',
            name='event_photos',
            field=models.ManyToManyField(null=True, to='web.EventsPhotos', blank=True, verbose_name='Event photos'),
        ),
    ]
