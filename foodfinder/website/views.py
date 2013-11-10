from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import render_to_response

from website.models import Event, EventForm

# Create your views here.

def home(request):
    events = Event.objects.all()
    return render_to_response('facebook.html', {
        'request': request,
        'events': events,
    })

def manage_event(request, event_id=None):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            # any other hooks we want to put here
            return redirect('home')

    elif event_id:
        e = Event.objects.filter(pk=event_id)[0]
        if e:
            form = EventForm(instance=e)
    else:
        form = EventForm()

    return render(request, 'manage_event.html', {
        'form': form
    })

def facebook(request):
    return render(request, 'facebook.html')

def channel(request):
    return render(request, 'channel.html')
