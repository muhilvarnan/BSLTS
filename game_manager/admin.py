from django.contrib import admin

from .models import Zone, District


class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone', 'contact_name', 'contact_phone_number', 'contact_email')


admin.site.register(Zone, ZoneAdmin)
admin.site.register(District, DistrictAdmin)
