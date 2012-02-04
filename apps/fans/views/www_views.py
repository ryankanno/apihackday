from django.template import RequestContext
from django.shortcuts import render_to_response 


def slash(request):
    return render_to_response('www/slash.html', {}, 
        context_instance=RequestContext(request))


def update(request):
    return render_to_response('www/slash.html', {}, 
        context_instance=RequestContext(request))
