import facebook as facebookAPI
import datetime
import json
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import render_to_response

from django.http import HttpResponse, HttpResponseNotAllowed

from website.models import Event, EventForm, Vote, VoteForm, User

from pytz import timezone
import pytz
from django.core.urlresolvers import resolve
# Create your views here.

def home(request):
    votes = Vote.objects.filter(voter_fbid = get_facebook_id(request))
    events = Event.objects.filter(food=True)
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
            'allDay' : False,
            'inPast': e.end_time.replace(tzinfo=None) < datetime.datetime.now(),
            'vote' : votes.get(event_id=e.id).was_food if votes.filter(event_id=e.id).exists() else None,          
            'map_url': e.image_url,
            'allDay' : False
        } for e in events]
    })
    current_url = resolve(request.path_info).url_name
    form = EventForm()
    return render(request, 'index.html', {
        'events_cal': events_cal,
        'request': request,
        'form' : form,
        'fb_id': get_facebook_id(request),
        'votes': votes,
        'current_url': current_url,
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
                event.creator_fbid = User.objects.get_or_create(fbid=get_facebook_id(request))[0]
                event.food = True
                event.save()
                print event
    return redirect('home')

def save_vote(request):
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            vote = form.save()
            json_data = json.dumps({"HTTPRESPONSE": 1,'glyph_val': vote.was_food})
            return HttpResponse(json_data, mimetype="application/json")
        else:
            print request.POST
            data = request.POST
            vote = Vote.objects.get(event_id = data['event_id'], voter_fbid = data['voter_fbid'])
            vote.was_food = data['was_food']
            vote.save()
            json_data = json.dumps({"HTTPRESPONSE": 1,'glyph_val': vote.was_food})
            return HttpResponse(json_data, mimetype="application/json")
        print request.POST
        data = json.dumps({'stuff': form.non_field_errors(), 'other_errors': form.errors.items()})
        return HttpResponse(data, mimetype="application/json")


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

def leaderboard(request):
    return render(request, 'leaderboards.html')


def get_facebook_id(request):
    """
    cached in request.session
    also adds to User table
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

    # add record to User table
    User.objects.get_or_create(fbid=profile['id'])

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
