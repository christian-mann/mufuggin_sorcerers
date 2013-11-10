from django.db import models
from django.forms import ModelForm

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=30)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=1000)
    notes = models.TextField(default='')

    creation_time = models.DateTimeField(auto_now_add=True)

    creator_fbid = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    @property
    def duration(self):
        return self.end_time - self.start_time


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'start_time', 'end_time', 'location', 'notes']
