from django.contrib import admin
from .models import CflTeam, TeamFantasyLeague, TeamFantasyTeam, Game, Stat, GameStatLog

admin.site.register(CflTeam)

admin.site.register(TeamFantasyLeague)

admin.site.register(TeamFantasyTeam)

admin.site.register(Game)

admin.site.register(Stat)

admin.site.register(GameStatLog)


