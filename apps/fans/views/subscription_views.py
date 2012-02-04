from django.template import RequestContext
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

    subscription = Subscription(league_id=league_id, team_id=team_id, game_id=game_id)
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
