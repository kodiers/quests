# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0014_auto_20150731_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.TextField(verbose_name='Title', blank=True, null=True)),
                ('description', models.TextField(verbose_name='Descrition', blank=True, null=True)),
                ('date', models.DateField(verbose_name='Date', blank=True, null=True)),
                ('image', models.ImageField(upload_to='images')),
            ],
            options={
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photos',
            },
        ),
        migrations.RemoveField(
            model_name='events',
            name='event_photos',
        ),
        migrations.DeleteModel(
            name='EventsPhotos',
        ),
        migrations.AddField(
            model_name='photos',
            name='event',
            field=models.ForeignKey(verbose_name='Event', to='web.Events', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='photos',
            name='user',
            field=models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL, blank=True, null=True),
        ),
    ]
