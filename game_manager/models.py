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


class District(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=255)
    contact_phone_number = models.CharField(max_length=255)
    contact_email = models.EmailField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Participant(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    code = models.CharField(max_length=255, default=random_string)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.code + " - " + self.name


class Team(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    code = models.CharField(max_length=255, default=random_string)
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(Participant)

    def __str__(self):
        return self.code + " - " + self.name

