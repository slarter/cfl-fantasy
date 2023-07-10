from django.core.management.base import BaseCommand
from django.conf import settings

from team_tracker.models import TeamFantasyTeam, TeamFantasyLeague, GameStatLog

class Command(BaseCommand):
    help = "Calculates the updated points for the given fantasy league"

    def add_arguments(self, parser):
        default_league = TeamFantasyLeague.objects.order_by('-id').first()
        league_name = default_league.name if default_league else ''
        parser.add_argument("league", nargs="?", type=str, default=league_name)

    def handle(self, *args, **options):
        print("===== Running calculate_fantasy_teams_points()")
        league_name = options['league']
        try:
            self.main(league_name)
        except Exception as e:
            print(f'calculate_fantasy_teams_points Error in main. {e}')
        print("===== Ended running calculate_fantasy_teams_points()")
    
    def main(self, league_name):
        league = TeamFantasyLeague.objects.filter(name=league_name).first()
        if not league:
            raise Exception(f'League "{league_name}" does not exist')
        
        fantasy_teams = TeamFantasyTeam.objects.filter(league=league)
        last_calculated_game_num = league.last_calculated_game.game_number if league.last_calculated_game else 0
        new_game_stats = GameStatLog.objects.filter(game__season=settings.CFL_SEASON, game__game_number__gt=last_calculated_game_num)
        
        for game_stat in new_game_stats:
            teams = [team for team in fantasy_teams if team.cfl_team == game_stat.cfl_team]
            for team in teams:
                team.points += game_stat.value * game_stat.stat.points
        
        updated_fantasy_teams = TeamFantasyTeam.objects.bulk_update(fantasy_teams, ['points'])
    
        