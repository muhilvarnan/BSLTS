from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django import forms

from .models import Zone, District, Participant, Team, Event, EventCriteria, EventParticipant, Samithi, Group, ParticipantFamily

MAX_EVENT_PER_PARTICIPANT = 2
MAX_PARTICIPANT_IN_TEAM = 5


class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', )


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone', 'contact_name', 'contact_phone_number', 'contact_email')
    search_fields = ('name', 'zone__name', 'contact_name', 'contact_phone_number', 'contact_email')


class TeamInline(admin.TabularInline):
    model = Team.participants.through


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


class ParticipantResource(resources.ModelResource):

    class Meta:
        model = Participant
        fields = ('name', 'date_of_birth', 'district', 'gender', 'samithi')

    def get_instance(self, instance_loader, row):
        try:
            row['samithi'] = Samithi.objects.get(name=row['samithi'], district__name__icontains=row['district']).id
            return None
        except District.DoesNotExist:
            pass
        except Samithi.DoesNotExist:
            pass


class ParticipantAdminForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('code', 'name', 'date_of_birth', 'gender', 'samithi', 'group', 'accommodation', 'arrival_point', 'arrival_date',
                  'arrival_time', 'departure_point', 'departure_date', 'departure_time')

    def clean_group(self):
        if self.cleaned_data['date_of_birth'] > self.cleaned_data['group'].max_dob or \
                self.cleaned_data['date_of_birth'] < self.cleaned_data['group'].min_dob:
            raise forms.ValidationError("Participant dob is not between the selected group min dob limit (%s)"
                                        " and max dob limit (%s) " %
                                        (str(self.cleaned_data['group'].min_dob),
                                        str(self.cleaned_data['group'].max_dob)))
        return self.cleaned_data['group']


class EventParticipantAdminForm(forms.ModelForm):
    class Meta:
        model = EventParticipant
        fields = ('event', 'team', 'participant')

    def check_mismatch_event_participant_count(self, participant):
        return participant.eventparticipant_set.count() >= MAX_EVENT_PER_PARTICIPANT

    def clean_participant(self):
        if self.cleaned_data['participant'] and self.check_mismatch_group(self.cleaned_data['participant']):
            raise self.get_group_mismatch_validation_error(self.cleaned_data['participant'])

        if self.cleaned_data['participant'] and self.check_mismatch_event_participant_count(self.cleaned_data['participant']):
            raise self.get_mismatch_event_participant_count_validation_error(self.cleaned_data['participant'])

        if self.cleaned_data['participant']:
            if EventParticipant.objects\
                    .filter(participant__samithi__district__id=self.cleaned_data['participant'].samithi.district.id,
                            event__id=self.cleaned_data['event'].id)\
                    .exclude(pk=self.instance.id):
                raise forms.ValidationError("Participant already exists for the event for the district %s" % (self.cleaned_data['participant'].samithi.district.name,))

        return self.cleaned_data['participant']

    def check_mismatch_group(self, participant):
        return participant.group.id not in list(map(lambda group: group.id, self.cleaned_data['event'].groups.all()))

    def get_group_mismatch_validation_error(self, participant):
        return forms.ValidationError("Participant with code %s is in Group(%s) which does not match with event group%s)"
                                     % (participant.code,
                                        participant.group.name,
                                        ",".join(map(lambda group: group.name, self.cleaned_data['event'].groups.all()))))

    def get_mismatch_event_participant_count_validation_error(self, participant):
        return forms.ValidationError("Participant with code %s is already reached max participation count %s"
                                     % (participant.code,
                                        str(MAX_EVENT_PER_PARTICIPANT)))

    def clean_team(self):
        if self.cleaned_data['team']:

            group_mismatch_participants = list(filter(self.check_mismatch_group,
                                                 self.cleaned_data['team'].participants.all()))
            if group_mismatch_participants:
                raise forms.ValidationError(list(map(self.get_group_mismatch_validation_error,
                                                     group_mismatch_participants)))

            event_participant_count_mismatch_participants = list(filter(self.check_mismatch_event_participant_count,
                                                 self.cleaned_data['team'].participants.all()))
            if event_participant_count_mismatch_participants:
                raise forms.ValidationError(list(map(self.get_mismatch_event_participant_count_validation_error,
                                                     event_participant_count_mismatch_participants)))
            if self.cleaned_data['team'] and self.cleaned_data['team'].participants.count():
                district = self.cleaned_data['team'].participants.first().samithi.district

                if EventParticipant.objects \
                        .filter(team__participants__samithi__district__id=district.id,
                                event__id=self.cleaned_data['event'].id) \
                        .exclude(pk=self.instance.id):
                    raise forms.ValidationError("Team already exists for the event for the district %s" % (
                    district.name,))

        return self.cleaned_data['team']


class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ('event', 'team', 'participant')
    search_fields = ('event__name', 'team__name', 'participant__name')
    list_filter = (('event__name', custom_titled_filter('Event')),)

    form = EventParticipantAdminForm


class EventParticipantInline(admin.TabularInline):
    model = EventParticipant
    fields = ('event',)
    form = EventParticipantAdminForm

class ParticipantFamilyAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'participant', 'relation')

class ParticipantFamilyInline(admin.TabularInline):
    model = ParticipantFamily
    fields = ('name', 'gender', 'relation')



class ParticipantAdmin(ImportExportModelAdmin):
    list_display = ('code', 'name', 'date_of_birth', 'samithi_district_name', 'samithi_district_zone', 'gender', 'samithi', 'group')
    search_fields = ('code', 'name', 'date_of_birth', 'samithi__district__name', 'samithi__district__zone__name', 'samithi__name', 'group__name')
    list_filter = (('samithi__district__name', custom_titled_filter('District')), ('samithi__name', custom_titled_filter('Samithi')), ('group__name', custom_titled_filter('Group')), 'gender')
    form = ParticipantAdminForm

    resource_class = ParticipantResource

    def samithi_district_zone(self, obj):
        return obj.samithi.district.zone.name

    def samithi_district_name(self, obj):
        return obj.samithi.district.name

    samithi_district_zone.short_description = 'District Zone'
    samithi_district_name.short_description = 'District'

    inlines = [
        ParticipantFamilyInline,
        TeamInline,
        EventParticipantInline
    ]


class TeamAdminForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('code', 'name', 'participants')

    def clean_participants(self):
        if self.cleaned_data['participants']:
            errors = []
            gender = None
            for participant in self.cleaned_data['participants']:
                if gender and gender != participant.gender:
                    errors.append(forms.ValidationError("Participants should be in same gender"))
                    break
                gender = participant.gender

            group = None
            for participant in self.cleaned_data['participants']:
                if group and group != participant.group.id:
                    errors.append(forms.ValidationError("Participants should be in same group"))
                group = participant.group.id

            district = None
            for participant in self.cleaned_data['participants']:
                if district and district != participant.samithi.district.id:
                    errors.append(forms.ValidationError("Participants should be in same district"))
                district = participant.samithi.district.id

            if self.cleaned_data['participants'].count() > MAX_PARTICIPANT_IN_TEAM:
                errors.append(forms.ValidationError("Team can only max of %s participants" % (MAX_PARTICIPANT_IN_TEAM,
                                                                                              )))

            if errors:
                raise forms.ValidationError(errors)

        return self.cleaned_data['participants']


class TeamAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'total_participants')
    search_fields = ('code', 'name')
    filter_horizontal = ('participants',)
    form = TeamAdminForm

    def total_participants(self, obj):
        return obj.participants.count()

    total_participants.empty_value_display = 0


class EventCriteriaInline(admin.TabularInline):
    model = EventCriteria


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'download_judge_sheet')
    search_fields = ('name',)
    list_filter = ('groups',)

    inlines = [
        EventCriteriaInline,
    ]

    def download_judge_sheet(self, obj):
        return format_html('<a href="%s/%s">%s</a>' % ('/game-manager/download/judge-sheet', obj.id, "Download"))

    download_judge_sheet.allow_tags = True


class EventCriteriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'max_mark')


class SamithiAdmin(admin.ModelAdmin):
    list_display = ('name', )


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_dob', 'min_dob')


admin.site.register(Zone, ZoneAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventCriteria, EventCriteriaAdmin)
admin.site.register(EventParticipant, EventParticipantAdmin)
admin.site.register(Samithi, SamithiAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(ParticipantFamily, ParticipantFamilyAdmin)


