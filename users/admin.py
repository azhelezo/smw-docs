from django.contrib import admin
from .models import Profile, Signature


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_hod', 'is_pur', 'is_fin', 'is_gm')
    search_fields = ('user',)
    list_filter = ('is_hod', 'is_pur', 'is_fin', 'is_gm')
    empty_value_display = '-пусто-'

class SignatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'approved',)
    empty_value_display = '-пусто-'

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Signature, SignatureAdmin)
