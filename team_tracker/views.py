from django.shortcuts import render
from django.http import HttpResponse

from team_tracker.models import *

def home(request):
    return render(request, 'team_tracker/home.html')


def standings(request):
    fantasy_teams = TeamFantasyTeam.objects.order_by('-points').all()
    context = {'fantasy_teams': fantasy_teams}

    return render(request, 'team_tracker/standings.html', context)

def info(request):
    tracked_stats = Stat.objects.all()
    context = {'tracked_stats': tracked_stats}

    return render(request, 'team_tracker/info.html', context)
