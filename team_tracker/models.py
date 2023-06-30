from django.db import models
from django.contrib.auth.models import User

class CflTeam(models.Model):
    name = models.CharField(max_length=100)
    name_short = models.CharField(max_length=100, default='')
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TeamFantasyLeague(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TeamFantasyTeam(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cfl_team = models.ForeignKey(CflTeam, on_delete=models.CASCADE)
    league = models.ForeignKey(TeamFantasyLeague, on_delete=models.CASCADE)
    points = models.FloatField(default=0)

    def __str__(self):
        return self.name

class Game(models.Model):
    date_start = models.DateField()
    week = models.IntegerField()
    season = models.IntegerField()
    home_team = models.ForeignKey(CflTeam, on_delete=models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey(CflTeam, on_delete=models.CASCADE, related_name='away_team')

    def __str__(self):
        return f'{self.home_team.name} vs. {self.away_team.name}'

class Stat(models.Model):
    name = models.CharField(max_length=100)
    points = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.name

class GameStatLog(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE)
    cfl_team = models.ForeignKey(CflTeam, on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return f'{self.stat.name} for {self.cfl_team.name} in game {self.game.id}'
    
