from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from web.models import QuestsUsers

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


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
