from django.contrib import admin

from .models import Zone, District, Participant, Team, Event, EventCriteria, EventParticipant, EventMark, Judge, Samithi


class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', )


class ParticipantInline(admin.TabularInline):
    model = Participant


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone', 'contact_name', 'contact_phone_number', 'contact_email')
    search_fields = ('name', 'zone__name', 'contact_name', 'contact_phone_number', 'contact_email')

    inlines = [
        ParticipantInline,
    ]


class TeamInline(admin.TabularInline):
    model = Team.participants.through


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'date_of_birth', 'district', 'district_zone', 'gender', 'samithi')
    search_fields = ('code', 'name', 'date_of_birth', 'district__name', 'district__zone__name', 'samithi__name')
    list_filter = (('district__name', custom_titled_filter('District')), ('samithi__name', custom_titled_filter('Samithi')), 'gender')

    def district_zone(self, obj):
        return obj.district.zone.name

    district_zone.admin_order_field = 'author__first_name'

    inlines = [
        TeamInline,
    ]


class TeamAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'total_participants')
    search_fields = ('code', 'name')

    def total_participants(self, obj):
        return obj.participants.count()

    total_participants.empty_value_display = 0


class EventCriteriaInline(admin.TabularInline):
    model = EventCriteria


class EventParticipantInline(admin.TabularInline):
    model = EventParticipant


class EventMarkInline(admin.TabularInline):
    fields = ('judge', 'event_participant', 'event_criteria', 'mark')

    model = EventMark


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')
    search_fields = ('name',)
    list_filter = ('group', )

    inlines = [
        EventCriteriaInline,
        EventParticipantInline,
        EventMarkInline
    ]


class EventCriteriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'max_mark')


class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ('event', 'team', 'participant', 'district', 'group')
    search_fields = ('event__name', 'team__name', 'participant__name')
    list_filter = (('event__name', custom_titled_filter('Event')),)

    def district(self, obj):
        return obj.participant.district

    def group(self, obj):
        return obj.event.get_group_display()

    district.empty_value_display = ""
    group.empty_value_display = ""


class JudgeAdmin(admin.ModelAdmin):

    list_display = ('name',)
    inlines = [
        EventMarkInline,
    ]


class EventMarkAdmin(admin.ModelAdmin):
    list_display = ('judge', 'event_participant', 'event_criteria', 'mark')

class SamithiAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Zone, ZoneAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventCriteria, EventCriteriaAdmin)
admin.site.register(EventParticipant, EventParticipantAdmin)
admin.site.register(EventMark, EventMarkAdmin)
admin.site.register(Judge, JudgeAdmin)
admin.site.register(Samithi, SamithiAdmin)

