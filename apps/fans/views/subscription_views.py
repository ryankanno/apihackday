from django.template import RequestContext
from django.shortcuts import render_to_response 
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json

from fans.models import Subscription

@csrf_exempt
def subscribe(request):
    output = {}

    league_id = request.POST.get('league_id', None)
    team_id   = request.POST.get('team_id', None)
    game_id   = request.POST.get('game_id', None)

    subscription = Subscription(league_id=league_id, team_id=team_id,
            game_id=game_id, created_by=request.user)
    subscription.save()

    output['subscription_id'] = subscription.pk

    return HttpResponse(json.dumps(output), mimetype="application/json")


@csrf_exempt
def unsubscribe(request):
    output = {}

    subscription_id = request.POST.get('subscription_id', None)
    sub = get_object_or_404(Subscription, id=subscription_id)

    if sub.league_id:
        output['league_id'] = sub.league_id

    if sub.team_id:
        output['team_id'] = sub.team_id

    if sub.game_id:
        output['game_id'] = sub.game_id

    sub.delete()

    return HttpResponse(json.dumps(output), mimetype="application/json")


def details(request):
    output = {}

    league_subs = Subscription.objects.get_league_subs(request.user)
    game_subs   = Subscription.objects.get_game_subs(request.user)
    team_subs   = Subscription.objects.get_team_subs(request.user)

    has_subs = league_subs.exists() or game_subs.exists() or team_subs.exists() 

    print has_subs

    return render_to_response('subscriptions/details.html', {'league_subs':
        league_subs, 'game_subs': game_subs, 'team_subs': team_subs, 'has_subs':
        has_subs}, 
        context_instance=RequestContext(request))
