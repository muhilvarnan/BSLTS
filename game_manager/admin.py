from django.contrib import admin

from .models import Zone, District, Participant, Team


class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone', 'contact_name', 'contact_phone_number', 'contact_email')


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'date_of_birth', 'district')


class TeamAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'total_participants')

    def total_participants(self, obj):
        return obj.participants.count()

    total_participants.empty_value_display = 0


admin.site.register(Zone, ZoneAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Team, TeamAdmin)

