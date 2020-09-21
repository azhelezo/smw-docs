from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import Order, Department


class OrderAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('id', 'requested_by', 'amount', 'date_created', 'all_signed', 'declined',)
    search_fields = ('text', 'requested_by',)
    list_filter = ('date_created', 'requested_by')
    empty_value_display = '-пусто-'

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name',)
    empty_value_display = '-пусто-'

admin.site.register(Order, OrderAdmin)
admin.site.register(Department, DepartmentAdmin)