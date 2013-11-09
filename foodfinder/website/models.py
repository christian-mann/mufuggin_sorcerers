from django.db import models

# Create your models here.

class Event(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=1000)
    notes = models.TextField()

    creation_time = models.DateTimeField(auto_now_add=True)

    @property
    def duration(self):
        return end_time - start_time
