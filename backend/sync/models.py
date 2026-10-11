from django.db import models


class Device(models.Model):
    """A device that syncs with the server, such as the shop PC."""

    name = models.CharField(max_length=100, unique=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
