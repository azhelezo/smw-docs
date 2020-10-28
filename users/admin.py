from django.contrib import admin
from .models import Profile, Signature


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', )
    search_fields = ('user',)
    list_filter = ('department', )
    empty_value_display = '-пусто-'

class SignatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'approved',)
    #empty_value_display = '-пусто-'

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Signature, SignatureAdmin)
