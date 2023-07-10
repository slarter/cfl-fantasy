from django.core.management.base import BaseCommand
from django.conf import settings

from time import sleep
import requests
from team_tracker.models import Game, CflTeam, Stat, GameStatLog

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("===== Running sync_games_to_db()")
        try:
            self.main()
        except Exception as e:
            print(f'sync_games_to_db Error in main. {e}')
        print("===== Ended running sync_games_to_db()")

    def main(self):
        last_stored_game_number = Game.objects.filter(season=settings.CFL_SEASON).order_by('-game_number').first()
        if last_stored_game_number is None:
            last_stored_game_number = 0
        
        r_params = f'sort=-date_start&filter[event_type_id][ne]=0&key={settings.CFL_API_KEY}'
        r = requests.get(f'http://api.cfl.ca/v1/games/{settings.CFL_season}?{r_params}')
        sleep(2)
        games = r.json()
        
        # save games
        for game in games.get('data'):
            if game.get('game_number') == last_stored_game_number:
                break

            r_params = f'include=boxscore&key={settings.CFL_API_KEY}'
            r = requests.get(f'http://api.cfl.ca/v1/games/{settings.CFL_season}/game/{game.get("game_id")}?{r_params}')

            api_game_json = r.json()
            api_game = api_game_json.get('data')[0]

            api_game_id = api_game.get('game_id')
            game_number = api_game.get('game_number')
            date_start = api_game.get('date_start').split('T')[0]
            week = api_game.get('week')
            season = api_game.get('season')
            team_1 = CflTeam.objects.filter(abbreviation=api_game.get('team_1').get('abbreviation')).first()
            team_2 = CflTeam.objects.filter(abbreviation=api_game.get('team_2').get('abbreviation')).first()
            team_1_points_allowed = api_game.get('team_2').get('score')
            team_2_points_allowed = api_game.get('team_1').get('score')
            winner = 'team_1' if team_1_points_allowed > team_2_points_allowed else 'team_2'

            db_game = Game(
                api_game_id = api_game_id,
                game_number = game_number,
                date_start = date_start,
                week = week,
                season = season,
                team_1 = team_1,
                team_2 = team_2
            )
            db_game.save()
            
            # save game stats
            game_stat_logs = []
            tracked_stats = Stat.objects.all()
            for team_num in ['team_1', 'team_2']:
                stat_value_dict = {stat.name: {'stat': stat, 'value': 0} for stat in Stat.objects.all()}
                team_boxscore = api_game.get('boxscore').get('teams').get(team_num)

                points_allowed = team_1_points_allowed if team_num == 'team_1' else team_2_points_allowed

                stat_value_dict['passing_yards_25']['value'] = round(float(team_boxscore.get('passing').get('pass_net_yards')) / 25, 2)
                stat_value_dict['rushing_yards_10']['value'] = round(float(team_boxscore.get('rushing').get('rush_net_yards')) / 10, 2)
                stat_value_dict['receiving_yards_10']['value'] = round(float(team_boxscore.get('receiving').get('receive_yards')) / 10, 2)
                stat_value_dict['passing_touchdowns']['value'] = team_boxscore.get('passing').get('pass_touchdowns')
                stat_value_dict['rushing_touchdowns']['value'] = team_boxscore.get('rushing').get('rush_touchdowns')
                stat_value_dict['receiving_touchdowns']['value'] = team_boxscore.get('receiving').get('receive_touchdowns')
                stat_value_dict['receptions']['value'] = team_boxscore.get('receiving').get('receive_caught')
                stat_value_dict['return_touchdowns']['value'] = team_boxscore.get('punt_returns').get('punt_returns_touchdowns') + team_boxscore.get('kick_returns').get('kick_returns_touchdowns')
                stat_value_dict['one_point_conversions']['value'] = team_boxscore.get('converts').get('one_point_converts').get('made')
                stat_value_dict['two_point_conversions']['value'] = team_boxscore.get('converts').get('two_point_converts').get('made')
                stat_value_dict['field_goals']['value'] = team_boxscore.get('field_goals').get('field_goal_made')
                stat_value_dict['interceptions_given']['value'] = team_boxscore.get('turnovers').get('interceptions')
                stat_value_dict['fumbles_lost']['value'] = team_boxscore.get('turnovers').get('fumbles')
                stat_value_dict['turnovers_on_downs']['value'] = team_boxscore.get('turnovers').get('downs')
                stat_value_dict['points_allowed_0']['value'] = int(points_allowed == 0)
                stat_value_dict['points_allowed_1_6']['value'] = int(1 <= points_allowed <= 6)
                stat_value_dict['points_allowed_7_13']['value'] = int(7 <= points_allowed <= 13)
                stat_value_dict['points_allowed_14_20']['value'] = int(14 <= points_allowed <= 20)
                stat_value_dict['points_allowed_21_27']['value'] = int(21 <= points_allowed <= 27)
                stat_value_dict['points_allowed_28_34']['value'] = int(28 <= points_allowed <= 34)
                stat_value_dict['points_allowed_35_plus']['value'] = int(points_allowed >= 35)
                stat_value_dict['sacks']['value'] = team_boxscore.get('defence').get('sacks_qb_made')
                stat_value_dict['interceptions_received']['value'] = team_boxscore.get('defence').get('interceptions')
                stat_value_dict['fumbles_recovered']['value'] = team_boxscore.get('defence').get('fumbles_recovered')
                stat_value_dict['defensive_safeties']['value'] = team_boxscore.get('defence').get('defensive_safeties')
                stat_value_dict['win']['value'] = int(winner == team_num)
                stat_value_dict['loss']['value'] = int(winner != team_num)

                for stat_value in stat_value_dict.values():
                    game_stat_logs.append(GameStatLog(
                        game = db_game,
                        stat = stat_value['stat'],
                        cfl_team = db_game.team_1 if team_num == 'team_1' else db_game.team_2,
                        value = stat_value['value'],
                    ))
            
            logs = GameStatLog.objects.bulk_create(game_stat_logs)
        
    


