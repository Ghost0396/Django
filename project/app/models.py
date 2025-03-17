from django.db import models


class Record(models.Model):
    """
    Model representing a record with various input fields and a timestamp.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=50)
    qr = models.CharField(max_length=50)
    station = models.CharField(max_length=50)
    failure = models.CharField(max_length=50)
    component = models.CharField(max_length=50)
    component_status = models.CharField(max_length=50)
    notes = models.CharField(max_length=50)
    component_repaired = models.CharField(max_length=50)
    summary = models.CharField(max_length=50)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the Record model.
        """
        return f"{self.created_at.strftime('%m/%d/%Y %H:%M')} - {self.user}"


class Configuration(models.Model):
    """
    Model representing configuration settings for generating reports.
    """
    file_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    users = models.CharField(max_length=50)

    def __str__(self):
        """
        String representation of the Configuration model.
        """
        return f"{self.file_name} - {self.email} - {self.users}"
