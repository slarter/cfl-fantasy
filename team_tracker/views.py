from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from team_tracker.models import *
import requests

def home(request):
    return render(request, 'team_tracker/home.html')


def standings(request):
    fantasy_teams = TeamFantasyTeam.objects.order_by('-points').all()
    context = {'fantasy_teams': fantasy_teams}

    return render(request, 'team_tracker/standings.html', context)

def load_game_stats_to_db(request):
    r = requests.get(f'http://api.cfl.ca/v1/games/2023?key={settings.CFL_API_KEY}')

    games = r.json()
    print(games)
    return HttpResponse("Games")

def get_team_points(request):
    return HttpResponse("Points")
