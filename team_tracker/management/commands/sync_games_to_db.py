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
            print(f'sync_games_to_db Error in main. {e}', exc_info=True)
        print("===== Ended running sync_games_to_db()")

    def main(self):
        last_stored_game_number = Game.objects.filter(season=settings.CFL_season).order_by('-game_number').first()
        r_params = f'sort=-date_start&filter[event_type_id][ne]=0&key={settings.CFL_API_KEY}'
        r = requests.get(f'http://api.cfl.ca/v1/games/{settings.CFL_season}?{r_params}')
        sleep(2)

        games = r.json()
        games = {
                "data":
                    [
                        {
                            "game_id":2172,
                            "date_start":"2015-06-08T19:30:00-04:00",
                            "game_number":1,
                            "week":1,
                            "season":2015,
                            "attendance":0,
                            "event_type":{
                                "event_type_id":0,
                                "name":"Preseason",
                                "title":""
                            },
                            "event_status":{
                                "event_status_id":4,
                                "name":"Final",
                                "is_active":False,
                                "quarter":4,
                                "minutes":0,
                                "seconds":0,
                                "down":3,
                                "yards_to_go":13
                            },
                            "venue":{
                                "venue_id":4,
                                "name":"Tim Hortons Field"
                            },
                            "weather":{
                                "temperature":21,
                                "sky":"Overcast",
                                "wind_speed":"",
                                "wind_direction":"6km\/h SW",
                                "field_conditions":"Dry"
                            },
                            "coin_toss":{
                                "coin_toss_winner":"",
                                "coin_toss_winner_election":"Ottawa won coin toss and elected to receive."
                            },
                            "tickets_url":"http:\/\/www.ticats.ca\/tickets\/",
                            "team_1":{
                                "team_id":6,
                                "location":"Ottawa",
                                "nickname":"Redblacks",
                                "abbreviation":"OTT",
                                "score":10,
                                "venue_id":6,
                                "linescores":[
                                {
                                    "quarter":1,
                                    "score":0
                                },
                                {
                                    "quarter":2,
                                    "score":0
                                },
                                {
                                    "quarter":3,
                                    "score":0
                                },
                                {
                                    "quarter":4,
                                    "score":10
                                }
                                ],
                                "is_at_home":False,
                                "is_winner":False
                            },
                            "team_2":{
                                "team_id":4,
                                "location":"Hamilton",
                                "nickname":"Tiger-Cats",
                                "abbreviation":"HAM",
                                "score":37,
                                "venue_id":4,
                                "linescores":[
                                {
                                    "quarter":1,
                                    "score":7
                                },
                                {
                                    "quarter":2,
                                    "score":13
                                },
                                {
                                    "quarter":3,
                                    "score":14
                                },
                                {
                                    "quarter":4,
                                    "score":3
                                }
                                ],
                                "is_at_home":True,
                                "is_winner":True
                            }
                        },
                        {
                            "game_id":2173,
                            "date_start":"2015-06-09T19:30:00-04:00",
                            "game_number":2,
                            "week":2,
                            "season":2015,
                            "attendance":5000,
                            "event_type":{
                                "event_type_id":0,
                                "name":"Preseason",
                                "title":""
                            },
                            "event_status":{
                                "event_status_id":4,
                                "name":"Final",
                                "is_active":False,
                                "quarter":4,
                                "minutes":0,
                                "seconds":0,
                                "down":1,
                                "yards_to_go":10
                            },
                            "venue":{
                                "venue_id":10,
                                "name":"Toronto: Varsity Stadium"
                            },
                            "weather":{
                                "temperature":16,
                                "sky":"Cloudy",
                                "wind_speed":"",
                                "wind_direction":"5 km per  hour",
                                "field_conditions":"Dry, artificial turf"
                            },
                            "coin_toss":{
                                "coin_toss_winner":"",
                                "coin_toss_winner_election":"Coin toss: Toronto won the toss and elected to receive."
                            },
                            "tickets_url":"http:\/\/www.argonauts.ca\/tickets\/",
                            "team_1":{
                                "team_id":9,
                                "location":"Winnipeg",
                                "nickname":"Blue Bombers",
                                "abbreviation":"WPG",
                                "score":34,
                                "venue_id":9,
                                "linescores":[
                                {
                                    "quarter":1,
                                    "score":3
                                },
                                {
                                    "quarter":2,
                                    "score":10
                                },
                                {
                                    "quarter":3,
                                    "score":14
                                },
                                {
                                    "quarter":4,
                                    "score":7
                                }
                                ],
                                "is_at_home":False,
                                "is_winner":True
                            },
                            "team_2":{
                                "team_id":8,
                                "location":"Toronto",
                                "nickname":"Argonauts",
                                "abbreviation":"TOR",
                                "score":27,
                                "venue_id":8,
                                "linescores":[
                                {
                                    "quarter":1,
                                    "score":6
                                },
                                {
                                    "quarter":2,
                                    "score":0
                                },
                                {
                                    "quarter":3,
                                    "score":8
                                },
                                {
                                    "quarter":4,
                                    "score":13
                                }
                                ],
                                "is_at_home":True,
                                "is_winner":False
                            }
                        },
                    ],
                "errors": [],
                "meta": {
                    "copyright":"Copyright 2017 Canadian Football League."
                }
        }
        
        # save games
        for game in games.get('data'):
            if game.get('game_number') == last_stored_game_number:
                break

            r_params = f'include=boxscore&key={settings.CFL_API_KEY}'
            r = requests.get(f'http://api.cfl.ca/v1/games/{settings.CFL_season}/game/{game.get("game_id")}?{r_params}')

            api_game_json = r.json()
            api_game = api_game_json.get('data')

            api_game_id = api_game.get('game_id')
            game_number = api_game.get('game_number')
            date_start = api_game.get('date_start')
            week = api_game.get('week')
            season = api_game.get('season')
            team_1 = CflTeam.objects.filter(abbreviation=api_game.get('team_1').get('abbreviation')).first()
            team_2 = CflTeam.objects.filter(abbreviation=api_game.get('team_2').get('abbreviation')).first()

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
            boxscore = api_game.get('boxscore')
            for team_num in ['team_1', 'team_2']:
                team_boxscore = boxscore.get('teams').get(team_num)
                
                passing_yards_25 = round(float(team_boxscore.get('passing').get('pass_net_yards')) / 25, 2)
                rushing_yards_10 = round(float(team_boxscore.get('rushing').get('rush_net_yards')) / 10, 2)
                receiving_yards_10 = round(float(team_boxscore.get('receiving').get('receive_yards')) / 10, 2)
                passing_touchdowns = team_boxscore.get('passing').get('pass_touchdowns')
                rushing_touchdowns = team_boxscore.get('rushing').get('rush_touchdowns')
                receiving_touchdowns = team_boxscore.get('receiving').get('receive_touchdowns')
                receptions = team_boxscore.get('receiving').get('receive_caught')
                return_touchdowns = team_boxscore.get('punt_returns').get('punt_returns_touchdowns') + team_boxscore.get('kick_returns').get('kick_returns_touchdowns')
                one_point_conversions = team_boxscore.get('converts').get('one_point_converts').get('made')
                two_point_conversions = team_boxscore.get('converts').get('two_point_converts').get('made')
                field_goals = team_boxscore.get('field_goals').get('field_goal_made')
                interceptions_given = team_boxscore.get('turnovers').get('interceptions')
                fumbles_lost = team_boxscore.get('turnovers').get('fumbles')
                turnovers_on_downs = team_boxscore.get('turnovers').get('downs')
                points_allowed_0 = 0
                points_allowed_1_6 = 0
                points_allowed_7_13 = 0
                points_allowed_14_20 = 0
                points_allowed_21_27 = 0
                points_allowed_28_34 = 0
                points_allowed_35_plus = 0
                sacks = 0
                interceptions_received = 0
                fumbles_recovered = 0
                touchdowns = 0
                defensive_safeties = 0
                win = 0
                loss = 0

                game_stat_logs.append(GameStatLog(
                    game = db_game,
                    stat = passing_yards_25,
                    cfl_team = db_game.team_1 if team_num == 'team_1' else db_game.team_2,
                    value = passing_yards_25,
                ))





