from django.contrib import admin

from pages.models import FAQ, Pages, Contacts

# Register your models here.
admin.site.register(FAQ)
admin.site.register(Pages)
admin.site.register(Contacts)
