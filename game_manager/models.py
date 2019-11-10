from django.db import models
import uuid
import random
import string


def random_string(string_length=5):
    """Generate a random string of fixed length """
    letters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for i in range(string_length))


class Zone(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Group(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    min_dob = models.DateField()
    max_dob = models.DateField()

    def __str__(self):
        return self.name


class District(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=255)
    contact_phone_number = models.CharField(max_length=255)
    contact_email = models.EmailField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Samithi(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.district.name + " - " + self.name


class Participant(models.Model):
    GENDERS =  (
        ('Boy', 'Boy'),
        ('Girl', 'Girl')
    )
    TRANSPORT_MODE = (
        ('Railway Station','Railway Station'),
        ('Old Bus Stand','Old Bus Stand'),
        ('New Bus Stand','New Bus Stand')
    )

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    code = models.CharField(max_length=255, default=random_string)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=4, choices=GENDERS, default=None)
    samithi = models.ForeignKey(Samithi, on_delete=models.CASCADE, default=None)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    accommodation = models.BooleanField(default=True)
    arrival_point = models.CharField(max_length=50, choices=TRANSPORT_MODE, default=None)
    departure_point = models.CharField(max_length=50, choices=TRANSPORT_MODE, default=None)
    arrival_time = models.CharField(max_length=50)
    departure_time = models.CharField(max_length=50)
    arrival_date = models.DateField()
    departure_date = models.DateField()

    def __str__(self):
        return self.code + " - " + self.name

class ParticipantFamily(models.Model):
    GENDERS = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    RELATIONS = (
        ('Family', 'Family'),
        ('Guru', 'Guru'),
        ('DEC', 'DEC'),
        ('SSSO member', 'SSSO member')
    )
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDERS, default=None)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    relation = models.CharField(max_length=100, choices=RELATIONS, default=None)
    phone_number = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    code = models.CharField(max_length=255, default=random_string)
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(Participant, blank=True)

    def __str__(self):
        return self.code + " - " + self.name


class Event(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    groups = models.ManyToManyField(Group, blank=True, help_text="Groups in which paritcipants may in for the event", verbose_name="Participant falling group")

    def __str__(self):
        return ",".join(map(lambda group: group.name, self.groups.all())) + " - " + self.name


class EventCriteria(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    max_mark = models.IntegerField()

    def __str__(self):
        return self.event.name + " - " + self.name + " - mark: " + str(self.max_mark)


class EventParticipant(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        if self.participant:
            return self.event.name + " - Participant - " + self.participant.code
        else:
            return self.event.name + " - Team - " + self.team.code

