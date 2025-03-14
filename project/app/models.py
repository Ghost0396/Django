from django.db import models


class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=50)
    input1 = models.CharField(max_length=50)
    input2 = models.CharField(max_length=50)
    input3 = models.CharField(max_length=50)
    input4 = models.CharField(max_length=50)
    input5 = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.created_at.strftime('%m/%d/%Y %H:%M')} - {self.user}"
