from django.db import models
from django.forms import ModelForm

from website import maps

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=1000)
    notes = models.TextField(default='')
    food = models.BooleanField(default=True)

    creation_time = models.DateTimeField(auto_now_add=True)

    creator_fbid = models.ForeignKey('User', blank = True, null = True)

    def __str__(self):
        return self.title

    @property
    def duration(self):
        return self.end_time - self.start_time

    @property
    def image_url(self):
        map_url = maps.name_to_map(self.location)
        print map_url, type(map_url)
        if map_url:
            return '/static/img/maps/%s.png' % map_url
        else:
            return map_url

class User(models.Model):
    fbid = models.CharField(max_length=100, primary_key = True)
    vote_total = models.IntegerField(default = 0)

    def __str__(self):
        return self.fbid

class EventForm(ModelForm):
    class Meta:
        model = Event
        #fields = ['title', 'start_time', 'end_time', 'location', 'notes']


class Vote(models.Model):
    """
    Represents an instance of someone voting on an event (good/bad)
    """
    class Meta:
        unique_together = ("event_id", "voter_fbid")

    event_id = models.ForeignKey(Event)
    voter_fbid = models.ForeignKey(User)

    was_food = models.BooleanField() # true means there was food at the event

    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.voter_fbid) + ' -> ' + str(self.event_id)

class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ['event_id', 'voter_fbid', 'was_food']
