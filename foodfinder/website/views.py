import facebook as facebookAPI
import json
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import render_to_response

from django.http import HttpResponse, HttpResponseNotAllowed

from website.models import Event, EventForm, User

from pytz import timezone
import pytz

# Create your views here.

def home(request):
    events = Event.objects.filter()
    bannedusers = User.objects.filter(vote_total__lt=-3)
    for banneduser in bannedusers:
        events = events.exclude(creator_fbid=banneduser.fbid)


    central = timezone('America/Chicago')

    events_cal = json.dumps({
        'events': [{
            'id': e.id,
            'title': e.title,
            'start': str(e.start_time.astimezone(central)),
            'end': str(e.end_time.astimezone(central)),
            'location': e.location,
            'notes': e.notes,
             
            'map_url': e.image_url,
            'allDay' : False
        } for e in events]
    })

    print events_cal

    form = EventForm()
    return render(request, 'index.html', {
        'events_cal': events_cal,
        'request': request,
        'form' : form,
        'fb_id': get_facebook_id(request),
    })

def add_event(request):
    """
    Requires logged-in-ness
    """

    if request.method == 'POST':
        if get_facebook_id(request):
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.creator_fbid = get_facebook_id(request)
                event.food = True
                event.save()
                print event
    return redirect('home')

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

def channel(request):
    return render(request, 'channel.html')


def get_facebook_id(request):
    """
    cached in request.session
    """

    print request.session.keys()
    print 'fb_id' in request.session

    if 'fb_id' in request.session:
        return request.session['fb_id']

    if 'fb_accesstoken' not in request.COOKIES:
        return None

    graph = facebookAPI.GraphAPI(request.COOKIES['fb_accesstoken'])
    profile = graph.get_object('me')
    request.session['fb_id'] = profile['id']

    return request.session['fb_id']

def create_event(request, **kwargs):
    # make sure we have the facebook ID
    cookies = request.COOKIES
    if 'fb_accesstoken' not in cookies:
        return render(request, 'facebook.html')

    print request.COOKIES
    fbid = get_facebook_id(request)
    print 'id: ' + fbid
    return HttpResponse("Good job, id #%s" % fbid)
