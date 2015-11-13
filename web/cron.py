__author__ = 'kodiers'

import kronos
import datetime
from quests.settings import EMAIL_HOST_USER
from web.models import Events, TodayEvents, EventStatistics, EventsWinners
from web.functions import send_user_notification
from django.db.models import Max, Min
from django.utils.translation import ugettext as _

@kronos.register('0 0 * * *')
def test_task():
    """
    Task for test kronos: Should be deleted
    :return:
    """
    print("Task success!")


@kronos.register('01 0 * * *')
def check_today_events():
    """
    Should run at 0:0 o'clock.
    Once at day check events< that are started today and place in temporary storage (TodayEvents model)
    If event end_date and started => then complete event.
    :return:
    """
    today = datetime.datetime.now()
    tomorrow = datetime.datetime.now() + datetime.timedelta(1)
    events = Events.objects.filter(start_date__gte=today).filter(started=False).filter(start_date__lt=tomorrow).filter(completed=False)
    completed_events = Events.objects.filter(end_date__lt=today).filter(started=True).filter(completed=False)
    if events:
        for event in events:
            today_event = TodayEvents()
            today_event.event = event
            today_event.start_time = event.start_date
            today_event.save()
            # Notify organizer
            org_subject = _("Your event %s begin today" % event.title)
            send_user_notification(org_subject, "", EMAIL_HOST_USER, event.organizer.email)
            # Notify players (teams)
            email_message = _("Event {event} begin today {date_time}".format(
                            event=event.title, date_time=event.start_date.strftime("%Y-%m-%d %H:%M")
                        ))
            if event.is_team:
                for team in event.registered_teams.all():
                    for player in team.players.all():
                        email_subject = _("You in team {team} that registered on event {event}".format(
                            team=team.title, event=event.title
                        ))
                        send_user_notification(email_subject, email_message, EMAIL_HOST_USER, player.email)
            else:
                # Notify players (not team events)
                email_subject = _("You are registered at event %s that begin today" % event.title)
                for player in event.registered_players.all():
                    send_user_notification(email_subject, email_message, EMAIL_HOST_USER, player.email)
    else:
        print("No events today")
    if completed_events:
        for completed_event in completed_events:
            completed_event.completed = True
            completed_event.started = False
            completed_event.save()
            max_event_score = EventStatistics.objects.filter(event=completed_event).aggregate(Max('score'))
            min_event_time = EventStatistics.objects.filter(event=completed_event).aggregate(Min('time'))
            if max_event_score['score__max']:
                if EventStatistics.objects.filter(event=completed_event).filter(time=min_event_time['time__min']).filter(score=max_event_score['score__max']).exists():
                    winner_eventstats = EventStatistics.objects.filter(event=completed_event).filter(time=min_event_time['time__min']).get(score=max_event_score['score__max'])
                    if not EventsWinners.objects.filter(eventstat=winner_eventstats).exists():
                        winner = EventsWinners()
                        winner.event = winner_eventstats.event
                        winner.eventstat = winner_eventstats
                        winner.player = winner_eventstats.player
                        winner.team = winner_eventstats.team
                        winner.save()




@kronos.register('*/5 * * * *')
def check_now_events():
    """
    Should run every 5 minutes.
    Check events in temporary storage (TodayEvents) that are started in 10 minutes and start it
    :return:
    """
    now = datetime.datetime.now()
    minutes = now + datetime.timedelta(0, 0, 0, 0, 10)
    today_events = TodayEvents.objects.filter(start_time__gte=now).filter(start_time__lte=minutes)
    if today_events:
        for event in today_events:
            event.event.started = True
            event.event.save()
            event.delete()




