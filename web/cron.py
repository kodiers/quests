__author__ = 'kodiers'

import kronos
import datetime
from web.models import Events, TodayEvents, EventStatistics, EventsWinners
from django.db.models import Max, Min

@kronos.register('0 0 * * *')
def test_task():
    """
    Task for test kronos: Should be deleted
    :return:
    """
    print("Task success!")


@kronos.register('0 0 * * *')
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




@kronos.register('0 0 * * *')
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




