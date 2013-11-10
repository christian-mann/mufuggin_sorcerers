from django.contrib import admin

from website.models import Event
from website.models import Vote

# Register your models here.

admin.site.register(Event)
admin.site.register(Vote)
