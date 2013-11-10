from django.shortcuts import render
from django.shortcuts import render_to_response

# Create your views here.

def home(request):
    events = Event.objects.all()
    return render_to_response('index.html', {
        'events': events
    })

