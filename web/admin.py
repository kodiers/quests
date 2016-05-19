from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from web.models import QuestsUsers, Contacts, Players, Tariffs, TariffsFeature, Organizers, Teams
from web.models import EventsPlaces, Events, Tasks, Hints, Photos
from web.models import EventStatistics, TaskStatistics, TodayEvents, EventsWinners

# Register your models here.
class QuestsUserInline(admin.StackedInline):
    """
    Define inline admin descriptor for QuestsUser model
    """
    model = QuestsUsers
    can_delete = False
    verbose_name = "QuestsUsers"
    readonly_fields = ('image_tag',)


class UserAdmin(UserAdmin):
    """
    Create a new UserAdmin class
    """
    inlines = (QuestsUserInline,)


class ContactsAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'phone', 'skype',)
    list_filter = ('country', 'user', )
    search_fields = ('user__username', 'country', 'street', 'city', 'skype')


class PlayersAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')
    list_filter = ('points',)
    search_fields = ('user__username', 'description')


class TariffsAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    list_filter = ('price',)
    search_fields = ('title', 'description')


class TariffsFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title', 'description', 'tariffs__title',)


class OrganizersAdmin(admin.ModelAdmin):
    list_display = ('user', 'tariff', 'show_on_main_page')
    list_filter = ('tariff', 'show_on_main_page')
    search_fields = ('user__username', 'description')


class TeamsAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'points')
    list_filter = ('points',)
    search_fields = ('players__username',)


class EventsPlacesAdmin(admin.ModelAdmin):
    list_display = ('country', 'city',)
    list_filter = ('country', 'city')
    search_fields = ('country', 'city', 'events__title')


class EventsAdmin(admin.ModelAdmin):
    """
    Admin model for events
    """
    list_display = ('title', 'is_team', 'price', 'completed', 'started')
    list_filter = ('is_team', 'completed', 'started', 'start_date', 'end_date')
    search_fields = ('title', 'description', 'organizer__username')
    date_hierarchy = 'start_date'
    readonly_fields = ('image_tag',)


class TasksAdmin(admin.ModelAdmin):
    list_display = ('title', 'score', 'event')
    list_filter = ('event',)
    search_fields = ('title', 'description', 'event__title')


class HintsAdmin(admin.ModelAdmin):
    list_display = ('task',)
    search_fields = ('task__title', 'text')


class PhotosAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'event')
    list_filter = ('user', 'event', 'date')
    search_fields = ('user__username', 'event__title', 'title', 'description')


class EventStatisticsAdmin(admin.ModelAdmin):
    list_display = ('event', 'start_time', 'end_time', 'completed', 'score')
    list_filter = ('event', 'start_time', 'end_time', 'completed')
    search_fields = ('event__title', 'player__username', 'team__title')


class TaskStatisticsAdmin(admin.ModelAdmin):
    list_display = ('task', 'start_time', 'end_time', 'completed', 'score', 'answered')
    list_filter = ('task', 'start_time', 'end_time', 'completed', 'answered')
    search_fields = ('task__title', 'player__username', 'team__title')


class TodayEventsAdmin(admin.ModelAdmin):
    list_display = ('event', 'start_time')
    list_filter = ('start_time',)


class EventsWinnerAdmin(admin.ModelAdmin):
    list_display = ('eventstat', 'player', 'team', 'event')
    list_filter = ('player__username', 'team__title')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Contacts, ContactsAdmin)
admin.site.register(Players, PlayersAdmin)
admin.site.register(Tariffs, TariffsAdmin)
admin.site.register(TariffsFeature, TariffsFeatureAdmin)
admin.site.register(Organizers, OrganizersAdmin)
admin.site.register(Teams, TeamsAdmin)
admin.site.register(EventsPlaces, EventsPlacesAdmin)
admin.site.register(Events, EventsAdmin)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(Hints, HintsAdmin)
admin.site.register(EventStatistics, EventStatisticsAdmin)
admin.site.register(TaskStatistics, TaskStatisticsAdmin)
admin.site.register(Photos, PhotosAdmin)
admin.site.register(TodayEvents, TodayEventsAdmin)
admin.site.register(EventsWinners, EventsWinnerAdmin)
