# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import durationfield.db.models.fields.duration


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0002_auto_20150624_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('country', models.CharField(verbose_name='Country', null=True, blank=True, max_length=255)),
                ('city', models.CharField(verbose_name='City', null=True, blank=True, max_length=255)),
                ('street', models.TextField(verbose_name='Street', null=True, blank=True)),
                ('phone', models.TextField(verbose_name='Phone number', null=True, blank=True)),
                ('skype', models.CharField(verbose_name='Skype', null=True, blank=True, max_length=255)),
                ('site', models.TextField(verbose_name='Web site', null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.TextField(verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('map_link', models.TextField(verbose_name='Link to map', null=True, blank=True)),
                ('is_team', models.BooleanField(verbose_name='Team only', default=False)),
                ('price', models.FloatField(verbose_name='Price', default=0.0)),
                ('max_players', models.IntegerField(verbose_name='Limit players', null=True, blank=True)),
                ('start_date', models.DateTimeField(verbose_name='Start date')),
                ('end_date', models.DateTimeField(verbose_name='End date')),
                ('completed', models.BooleanField(verbose_name='Finished', default=False)),
                ('duration', durationfield.db.models.fields.duration.DurationField(verbose_name='Duration', null=True, blank=True)),
                ('organizer', models.ForeignKey(related_name='organizer', to=settings.AUTH_USER_MODEL, verbose_name='Organizer')),
            ],
            options={
                'verbose_name': 'Event',
                'ordering': ('start_date',),
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='EventsPlaces',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('country', models.CharField(verbose_name='Country', null=True, blank=True, max_length=255)),
                ('city', models.CharField(verbose_name='City', null=True, blank=True, max_length=255)),
                ('street', models.TextField(verbose_name='Street', null=True, blank=True)),
                ('lat', models.FloatField(verbose_name='Latitude', null=True, blank=True)),
                ('lon', models.FloatField(verbose_name='Longtitude', null=True, blank=True)),
                ('map_link', models.TextField(verbose_name='Link to map', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Event and task place',
                'verbose_name_plural': 'Event and task places',
            },
        ),
        migrations.CreateModel(
            name='EventStatistics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('score', models.IntegerField(verbose_name='Score', null=True, blank=True)),
                ('time', durationfield.db.models.fields.duration.DurationField(verbose_name='Executed time', null=True, blank=True)),
                ('event', models.ForeignKey(to='web.Events', verbose_name='Event')),
                ('player', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, verbose_name='Player', blank=True)),
            ],
            options={
                'verbose_name': 'Event statistic',
                'ordering': ('time',),
                'verbose_name_plural': 'Events statistics',
            },
        ),
        migrations.CreateModel(
            name='Hints',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('text', models.TextField(verbose_name='Text')),
                ('price', models.FloatField(verbose_name='Price', default=0.0)),
            ],
            options={
                'verbose_name': 'Hint',
                'verbose_name_plural': 'Hints',
            },
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('text', models.TextField(verbose_name='Text')),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('from_user', models.ForeignKey(related_name='from_user', to=settings.AUTH_USER_MODEL, verbose_name='From')),
                ('to_user', models.ForeignKey(related_name='to_user', to=settings.AUTH_USER_MODEL, verbose_name='To')),
            ],
            options={
                'verbose_name': 'Message',
                'ordering': ('date',),
                'verbose_name_plural': 'Messages',
            },
        ),
        migrations.CreateModel(
            name='Organizers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('description', models.TextField(verbose_name='Description', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Organizer',
                'verbose_name_plural': 'Organizers',
            },
        ),
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('description', models.TextField(verbose_name='Description', null=True, blank=True)),
                ('sex', models.IntegerField(verbose_name='Sex', choices=[(0, 'MALE'), (1, 'FEMALE'), (2, 'NOT DEFINED')], default=2)),
                ('date_of_birth', models.DateField(verbose_name='Date of birth', null=True, blank=True)),
                ('points', models.IntegerField(verbose_name='Points', default=0)),
                ('rating', models.IntegerField(verbose_name='Place (rating)', default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Player',
                'verbose_name_plural': 'Players',
            },
        ),
        migrations.CreateModel(
            name='Tariffs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('description', models.TextField(verbose_name='Description', null=True, blank=True)),
                ('price', models.FloatField(verbose_name='Price', default=0.0)),
            ],
            options={
                'verbose_name': 'Tariff',
                'ordering': ('price',),
                'verbose_name_plural': 'Tariffs',
            },
        ),
        migrations.CreateModel(
            name='TariffsFeature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.TextField(verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description', null=True, blank=True)),
                ('tariffs', models.ManyToManyField(to='web.Tariffs', verbose_name='Tariff')),
            ],
            options={
                'verbose_name': 'Tariff feature',
                'verbose_name_plural': 'Tariff features',
            },
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.TextField(verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('map_link', models.TextField(verbose_name='Link to map', null=True, blank=True)),
                ('score', models.IntegerField(verbose_name='Score', default=0)),
                ('answer', models.TextField(verbose_name='Answer', null=True)),
                ('event', models.ForeignKey(to='web.Events', verbose_name='Event')),
                ('place', models.ForeignKey(null=True, to='web.EventsPlaces', verbose_name='Place', blank=True)),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
            },
        ),
        migrations.CreateModel(
            name='TaskStatistics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('score', models.IntegerField(verbose_name='Score', null=True, blank=True)),
                ('time', durationfield.db.models.fields.duration.DurationField(verbose_name='Executed time', null=True, blank=True)),
                ('used_hints', models.IntegerField(verbose_name='Count of used hints', default=0)),
                ('player', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, verbose_name='Player', blank=True)),
                ('task', models.ForeignKey(to='web.Tasks', verbose_name='Task')),
            ],
            options={
                'verbose_name': 'Event statistic',
                'ordering': ('time',),
                'verbose_name_plural': 'Events statistics',
            },
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('points', models.IntegerField(verbose_name='Total points', default=0)),
                ('players', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Team',
                'verbose_name_plural': 'Teams',
            },
        ),
        migrations.AlterField(
            model_name='questsusers',
            name='image',
            field=models.ImageField(verbose_name='Avatar', null=True, blank=True, upload_to='avatars'),
        ),
        migrations.AlterField(
            model_name='questsusers',
            name='is_organizer',
            field=models.BooleanField(verbose_name='Organizer', default=False),
        ),
        migrations.AddField(
            model_name='taskstatistics',
            name='team',
            field=models.ForeignKey(null=True, to='web.Teams', verbose_name='Team', blank=True),
        ),
        migrations.AddField(
            model_name='organizers',
            name='tariff',
            field=models.ForeignKey(to='web.Tariffs', verbose_name='Tariff'),
        ),
        migrations.AddField(
            model_name='organizers',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hints',
            name='task',
            field=models.OneToOneField(to='web.Tasks'),
        ),
        migrations.AddField(
            model_name='eventstatistics',
            name='team',
            field=models.ForeignKey(null=True, to='web.Teams', verbose_name='Team', blank=True),
        ),
        migrations.AddField(
            model_name='events',
            name='place',
            field=models.ForeignKey(null=True, to='web.EventsPlaces', verbose_name='Place', blank=True),
        ),
        migrations.AddField(
            model_name='events',
            name='registered_players',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Regitered users', related_name='regitered_players'),
        ),
        migrations.AddField(
            model_name='events',
            name='registered_teams',
            field=models.ManyToManyField(to='web.Teams', verbose_name='Registered teams'),
        ),
    ]
