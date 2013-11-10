import facebook as facebookAPI
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import render_to_response

from django.http import HttpResponse, HttpResponseNotAllowed

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


def get_facebook_id(request):
    """
    cached in request.session
    """

    if 'fb_accesstoken' not in request.COOKIES:
        return None
    if 'fb_id' not in request.session or \
            'fb_accesstoken' not in request.session or \
            request.COOKIES['fb_accesstoken'] != request.session['fb_accesstoken']:
        # cache invalidation or something
        graph = facebookAPI.GraphAPI(request.COOKIES['fb_accesstoken'])
        profile = graph.get_object('me')
        
        request.session['fb_accesstoken'] = request.COOKIES['fb_accesstoken']
        request.session['fb_id'] = profile['id']

    # return cached value
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
