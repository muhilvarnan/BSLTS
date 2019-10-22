from django.db import models
import uuid


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
