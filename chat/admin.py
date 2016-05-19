from django.contrib import admin
from chat.models import Chat, Messages

# Register your models here.


class ChatAdmin(admin.ModelAdmin):
    list_display = ('pk', "have_new_message", )
    list_filter = ("have_new_message", )


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('sender', 'chat', 'new', 'datetime')
    list_filter = ('chat', 'new', 'datetime', 'sender')
    search_fields = ('text', 'sender__username')
    date_hierarchy = 'datetime'
    ordering = ['datetime']


admin.site.register(Chat, ChatAdmin)
admin.site.register(Messages, MessagesAdmin)



