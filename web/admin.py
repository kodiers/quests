from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from web.models import QuestsUsers, Contacts, Players, Tariffs, TariffsFeature, Organizers, Teams
from web.models import Messages, EventsPlaces, Events, Tasks, Hints, Photos
from web.models import EventStatistics, TaskStatistics

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


class EventsAdmin(admin.ModelAdmin):
    """
    Admin model for events
    """
    readonly_fields = ('image_tag',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Contacts)
admin.site.register(Players)
admin.site.register(Tariffs)
admin.site.register(TariffsFeature)
admin.site.register(Organizers)
admin.site.register(Teams)
admin.site.register(Messages)
admin.site.register(EventsPlaces)
admin.site.register(Events, EventsAdmin)
admin.site.register(Tasks)
admin.site.register(Hints)
admin.site.register(EventStatistics)
admin.site.register(TaskStatistics)
admin.site.register(Photos)