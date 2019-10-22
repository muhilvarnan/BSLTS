from django.contrib import admin

from .models import Zone, District, Participant, Team, Event, EventCriteria, EventParticipant, EventMark


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


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')


class EventCriteriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'max_mark')


class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ('event', 'team', 'participant')


class EventMarkAdmin(admin.ModelAdmin):
    list_display = ('judge_name', 'event_participant', 'event_criteria', 'mark')


admin.site.register(Zone, ZoneAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventCriteria, EventCriteriaAdmin)
admin.site.register(EventParticipant, EventParticipantAdmin)
admin.site.register(EventMark, EventMarkAdmin)

