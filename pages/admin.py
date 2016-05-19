from django.contrib import admin

from pages.models import FAQ, Pages, Contacts

# Register your models here.


class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'created')
    list_filter = ('created',)
    search_fields = ('question', 'answer')
    date_hierarchy = 'created'
    ordering = ['created']


class PagesAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'created')
    list_filter = ('created', )
    search_fields = ('title', 'content', 'ceo_keywords', 'ceo_description')
    prepopulated_fields = {'url': ('title',)}
    date_hierarchy = 'created'
    ordering = ['created']


class ContactsAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'url')
    search_fields = ('phone', 'url', 'comments', 'address')


admin.site.register(FAQ, FaqAdmin)
admin.site.register(Pages, PagesAdmin)
admin.site.register(Contacts, ContactsAdmin)
