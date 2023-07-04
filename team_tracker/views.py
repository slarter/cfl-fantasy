from django.shortcuts import render
from django.http import HttpResponse

from team_tracker.models import *

def home(request):
    return render(request, 'team_tracker/home.html')


def standings(request):
    fantasy_teams = TeamFantasyTeam.objects.order_by('-points').all()
    context = {'fantasy_teams': fantasy_teams}

    return render(request, 'team_tracker/standings.html', context)

def get_team_points(request):
    return HttpResponse("Points")
